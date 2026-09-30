"""
CIPHER-SENTINEL: Core analysis service.

Bridges the existing core engine (c:\\Users\\AS\\Downloads\\vpn\\core\\) to the
FastAPI layer. All heavy computation is done synchronously inside a threadpool
executor via asyncio.run_in_executor so it does not block the event loop.

Public API
----------
analyze_pcap_bytes(pcap_bytes, filename) -> dict
parse_config_file(content, vendor)       -> dict
generate_remediation(tunnel_name, local_ip, remote_ip) -> dict
"""

from __future__ import annotations

import logging
import os
import struct
import sys
import tempfile
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Ensure the vpn root (parent of 'core') is on sys.path so that all core
# modules can be imported regardless of where uvicorn is launched from.
# ---------------------------------------------------------------------------
_VPN_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
# __file__ = c:\Users\AS\Downloads\vpn\backend\services\analyzer.py
# two levels up  → c:\Users\AS\Downloads\vpn
_VPN_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _VPN_ROOT not in sys.path:
    sys.path.insert(0, _VPN_ROOT)

# ---------------------------------------------------------------------------
# Lazy imports of core engine (may not be importable in CI without deps)
# ---------------------------------------------------------------------------
try:
    from core.dissector.ike_parser import IKEPacketDissector          # type: ignore
    from core.dissector.esp_analyzer import ESPTrafficAnalyzer         # type: ignore
    from core.formal.z3_verifier import (                              # type: ignore
        NeuroSymbolicVerifier,
        ComplianceFinding,
    )
    from core.ai.pq_threat_engine import PostQuantumThreatEngine       # type: ignore
    from core.remediation.patch_generator import RemediationSynthesizer  # type: ignore
    _CORE_AVAILABLE = True
except ImportError as _import_err:
    logger.warning("Core engine modules not importable: %s", _import_err)
    _CORE_AVAILABLE = False


# ===========================================================================
# Internal helpers (mirrored from cipher_sentinel_cli.py)
# ===========================================================================

class _PCAPReader:
    """Zero-dependency Libpcap stream reader (clone of CLI version)."""

    @staticmethod
    def read_packets(filepath: str) -> List[bytes]:
        packets: List[bytes] = []
        if not os.path.exists(filepath):
            return packets
        with open(filepath, "rb") as f:
            global_hdr = f.read(24)
            if len(global_hdr) < 24:
                return packets
            magic = struct.unpack("!I", global_hdr[:4])[0]
            is_little_endian = magic == 0xD4C3B2A1
            fmt = "<IIII" if is_little_endian else "!IIII"
            while True:
                hdr_bytes = f.read(16)
                if len(hdr_bytes) < 16:
                    break
                ts_sec, ts_usec, incl_len, orig_len = struct.unpack(fmt, hdr_bytes)
                pkt_data = f.read(incl_len)
                if len(pkt_data) < incl_len:
                    break
                packets.append(pkt_data)
        return packets


def _extract_ipsec_payloads(raw_packet: bytes) -> Dict[str, Any]:
    """Extract UDP 500/4500 (IKE) or Protocol 50 (ESP) from raw Ethernet frame."""
    if len(raw_packet) < 34:  # Eth (14) + IPv4 min (20)
        return {}
    ethertype = struct.unpack("!H", raw_packet[12:14])[0]
    if ethertype != 0x0800:
        return {}
    ip_hdr = raw_packet[14:34]
    proto = ip_hdr[9]
    src_ip = ".".join(map(str, ip_hdr[12:16]))
    dst_ip = ".".join(map(str, ip_hdr[16:20]))
    ihl = (ip_hdr[0] & 0x0F) * 4
    l4_data = raw_packet[14 + ihl :]
    if proto == 17:  # UDP
        if len(l4_data) < 8:
            return {}
        src_port, dst_port, udp_len = struct.unpack("!HHH", l4_data[:6])
        udp_payload = l4_data[8:udp_len]
        if src_port in (500, 4500) or dst_port in (500, 4500):
            return {"type": "IKE", "src": src_ip, "dst": dst_ip, "port": dst_port, "payload": udp_payload}
    elif proto == 50:  # ESP
        return {"type": "ESP", "src": src_ip, "dst": dst_ip, "payload": l4_data}
    return {}


# ===========================================================================
# Public API
# ===========================================================================

def analyze_pcap_bytes(pcap_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Main bridge: accepts raw PCAP bytes, runs the full CIPHER-SENTINEL
    analysis pipeline, and returns a structured result dict.

    Returns
    -------
    dict with keys:
        proposals       – list of IKE proposal dicts
        findings        – list of finding dicts (from ComplianceFinding)
        posture         – security posture score dict
        pq_risk         – post-quantum risk dict
        esp_results     – ESP side-channel analysis dict or None
        exchange_name   – IKE exchange type string
        error           – error message string (only present on failure)
    """
    if not _CORE_AVAILABLE:
        logger.error("Core engine not available; returning stub result.")
        return _stub_result("Core engine modules not installed in this environment.")

    tmp_path: str | None = None
    try:
        # Write bytes to a named temp file so PCAPReader can open it
        with tempfile.NamedTemporaryFile(suffix=".pcap", delete=False) as tmp:
            tmp.write(pcap_bytes)
            tmp_path = tmp.name

        packets = _PCAPReader.read_packets(tmp_path)
        if not packets:
            return _stub_result(f"No packets found in file: {filename}")

        ike_payloads: List[Dict[str, Any]] = []
        esp_packets: List[bytes] = []

        for pkt in packets:
            extracted = _extract_ipsec_payloads(pkt)
            if extracted.get("type") == "IKE":
                ike_payloads.append(extracted)
            elif extracted.get("type") == "ESP":
                esp_packets.append(extracted["payload"])

        logger.info(
            "PCAP %s: %d total packets, %d IKE, %d ESP",
            filename,
            len(packets),
            len(ike_payloads),
            len(esp_packets),
        )

        # --- ESP analysis (no key required) ---
        esp_results = ESPTrafficAnalyzer.analyze_esp_stream(esp_packets) if esp_packets else None

        # --- IKE analysis ---
        parsed_proposals: List[Dict[str, Any]] = []
        exchange_name = "Unknown"

        for ike_item in ike_payloads:
            hdr = IKEPacketDissector.parse_header(ike_item["payload"])
            if hdr:
                exchange_name = hdr.get("exchange_type_name", "Unknown")
                props = IKEPacketDissector.dissect_proposals(hdr)
                if props:
                    parsed_proposals.extend(props)

        findings_dicts: List[Dict[str, Any]] = []
        posture: Dict[str, Any] = {
            "posture_score": 50,
            "classification": "UNKNOWN",
            "critical_violations": 0,
            "high_violations": 0,
            "medium_violations": 0,
        }
        pq_risk: Dict[str, Any] = {}

        if parsed_proposals:
            primary = parsed_proposals[0]
            raw_findings: List[ComplianceFinding] = NeuroSymbolicVerifier.verify_proposal(
                primary, exchange_name
            )
            posture = NeuroSymbolicVerifier.calculate_security_posture_score(raw_findings)
            pq_risk = PostQuantumThreatEngine.evaluate_quantum_risk(primary)

            for f in raw_findings:
                findings_dicts.append(
                    {
                        "rule_id": f.rule_id,
                        "severity": f.severity,
                        "standard": f.standard,
                        "violation": f.violation,
                        "impact": f.impact,
                        "remediation_goal": f.remediation_goal,
                    }
                )

        return {
            "proposals": parsed_proposals,
            "findings": findings_dicts,
            "posture": posture,
            "pq_risk": pq_risk,
            "esp_results": esp_results,
            "exchange_name": exchange_name,
        }

    except Exception as exc:
        logger.exception("analyze_pcap_bytes failed for %s", filename)
        return _stub_result(str(exc))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def parse_config_file(content: str, vendor: str) -> Dict[str, Any]:
    """
    Keyword-based static analysis of a VPN configuration file.

    Returns a dict with:
        findings      – list of finding dicts
        posture       – posture score dict
        vendor        – echoed vendor string
        raw_flags     – list of flagged keyword matches
    """
    findings: List[Dict[str, Any]] = []
    flags: List[str] = []

    content_upper = content.upper()

    # --- Weak encryption ---
    weak_enc = [
        ("DES ", "RULE-CFG-001", "CRITICAL", "DES encryption detected",
         "DES is deprecated (56-bit key). Trivially broken.", "Replace with AES-256-GCM."),
        ("3DES", "RULE-CFG-002", "CRITICAL", "3DES (Triple-DES) detected",
         "Birthday collision attack after 32 GB of traffic (CVE-2016-2183).", "Replace with AES-256-GCM."),
        ("MD5", "RULE-CFG-003", "CRITICAL", "MD5 hash algorithm detected",
         "Practical collision attacks allow signature forgery.", "Upgrade to SHA-384 or SHA-512."),
        ("SHA1", "RULE-CFG-004", "HIGH", "SHA-1 hash algorithm detected",
         "SHA-1 has been shattered; collision feasible (SHAttered).", "Upgrade to SHA-256 or higher."),
        ("SHA-1", "RULE-CFG-004", "HIGH", "SHA-1 hash algorithm detected",
         "SHA-1 has been shattered; collision feasible (SHAttered).", "Upgrade to SHA-256 or higher."),
        ("DH-GROUP 2", "RULE-CFG-005", "CRITICAL", "DH Group 2 (1024-bit MODP) detected",
         "Logjam attack; 1024-bit discrete log is precomputable by nation-states.", "Use DH Group 19/20 (ECP)."),
        ("GROUP 1", "RULE-CFG-006", "CRITICAL", "DH Group 1 (768-bit MODP) detected",
         "Below federal minimum; trivially broken.", "Use DH Group 19/20 (ECP)."),
        ("AGGRESSIVE", "RULE-CFG-007", "CRITICAL", "IKEv1 Aggressive Mode detected",
         "PSK hash sent in clear; enables offline GPU brute-force.", "Migrate to IKEv2 with certificate auth."),
        ("IKE VERSION 1", "RULE-CFG-008", "HIGH", "IKEv1 protocol detected",
         "IKEv1 lacks PFS by default and has known vulnerabilities.", "Upgrade to IKEv2."),
        ("IKEV1", "RULE-CFG-008", "HIGH", "IKEv1 protocol detected",
         "IKEv1 lacks PFS by default and has known vulnerabilities.", "Upgrade to IKEv2."),
        ("PSK", "RULE-CFG-009", "MEDIUM", "Pre-Shared Key authentication detected",
         "PSK is vulnerable to offline dictionary attacks if weak.", "Use certificate-based (PKI) authentication."),
        ("AES-128", "RULE-CFG-010", "MEDIUM", "AES-128 encryption detected",
         "Grover's algorithm halves symmetric security to 64 bits.", "Upgrade to AES-256-GCM."),
        ("NULL", "RULE-CFG-011", "CRITICAL", "NULL encryption (ESP-NULL) may be present",
         "Unencrypted ESP traffic is readable by passive observers.", "Enable AES-256-GCM encryption."),
    ]

    seen_rule_ids: set = set()
    for keyword, rule_id, severity, violation, impact, remediation_goal in weak_enc:
        if keyword in content_upper and rule_id not in seen_rule_ids:
            seen_rule_ids.add(rule_id)
            flags.append(keyword)
            findings.append(
                {
                    "rule_id": rule_id,
                    "severity": severity,
                    "standard": "NIST SP 800-77r1 / BSI TR-02102-3",
                    "violation": violation,
                    "impact": impact,
                    "remediation_goal": remediation_goal,
                }
            )

    # Compute a simple posture score
    score = 100
    penalties = {"CRITICAL": 35, "HIGH": 15, "MEDIUM": 5}
    for f in findings:
        score -= penalties.get(f["severity"], 0)
    score = max(0, score)

    critical = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high = sum(1 for f in findings if f["severity"] == "HIGH")
    medium = sum(1 for f in findings if f["severity"] == "MEDIUM")

    posture_class = (
        "DEFENSE_GRADE" if score >= 90
        else "ACCEPTABLE" if score >= 70
        else "VULNERABLE" if score >= 40
        else "COMPROMISED"
    )

    return {
        "findings": findings,
        "posture": {
            "posture_score": score,
            "classification": posture_class,
            "critical_violations": critical,
            "high_violations": high,
            "medium_violations": medium,
        },
        "vendor": vendor,
        "raw_flags": flags,
    }


def generate_remediation(
    tunnel_name: str = "NTRO-SECURE-GW",
    local_ip: str = "192.168.1.1",
    remote_ip: str = "192.168.1.2",
) -> Dict[str, Any]:
    """
    Generate multi-vendor hardened remediation configs via RemediationSynthesizer.

    Returns a dict whose values are the raw configuration strings:
        strongswan_swanctl
        cisco_iosxe
        fortinet_fortios
        ansible_playbook
    """
    if not _CORE_AVAILABLE:
        return {"error": "Core engine not available."}
    try:
        patches = RemediationSynthesizer.generate_all_patches(tunnel_name, local_ip, remote_ip)
        return patches
    except Exception as exc:
        logger.exception("generate_remediation failed")
        return {"error": str(exc)}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _stub_result(error_msg: str) -> Dict[str, Any]:
    return {
        "proposals": [],
        "findings": [],
        "posture": {
            "posture_score": 0,
            "classification": "ERROR",
            "critical_violations": 0,
            "high_violations": 0,
            "medium_violations": 0,
        },
        "pq_risk": {},
        "esp_results": None,
        "exchange_name": "Unknown",
        "error": error_msg,
    }
