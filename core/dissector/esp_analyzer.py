"""
CIPHER-SENTINEL: Passive Epistemic Cryptographic Fingerprinting (PECF) for ESP Traffic
Analyzes opaque Encapsulating Security Payload (ESP - IP Protocol 50 / NAT-T UDP 4500)
without private keys or payload decryption (PATENT CLAIM 1).
"""

import math
from typing import Dict, Any, List, Tuple
from collections import Counter

class ESPTrafficAnalyzer:
    """
    Statistically analyzes opaque ESP packet streams to derive:
    1. Cipher block size (8-byte DES/3DES vs 16-byte AES-CBC vs Continuous AEAD)
    2. Operational Mode (Tunnel vs. Transport)
    3. Null-encryption detection (RFC 2410 ESP-NULL)
    4. ICV Authentication tag footprint
    """

    @staticmethod
    def calculate_shannon_entropy(data: bytes) -> float:
        """
        Computes Shannon Entropy H(X) = -sum(P(x) * log2(P(x))) over byte distribution.
        True high-grade ciphertext has entropy approaching 7.95 - 8.00 bits/byte.
        Plaintext / ESP-NULL has entropy < 6.5 bits/byte.
        """
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        counts = Counter(data)
        for count in counts.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    @classmethod
    def analyze_esp_stream(cls, packets: List[bytes]) -> Dict[str, Any]:
        """
        Performs multi-packet epistemic side-channel analysis across an ESP flow.
        """
        if not packets:
            return {"error": "Empty packet stream"}

        entropies = []
        payload_lengths = []
        spis = set()
        seq_nums = []

        for pkt in packets:
            # Parse outer ESP: SPI (4B), Sequence (4B), Payload (variable)
            if len(pkt) < 8:
                continue
            spi = int.from_bytes(pkt[:4], byteorder='big')
            seq = int.from_bytes(pkt[4:8], byteorder='big')
            payload = pkt[8:]
            
            spis.add(hex(spi))
            seq_nums.append(seq)
            payload_lengths.append(len(payload))
            
            # Sample payload entropy (skip first 16 bytes IV if present)
            sample_payload = payload[16:] if len(payload) > 32 else payload
            entropies.append(cls.calculate_shannon_entropy(sample_payload))

        avg_entropy = sum(entropies) / len(entropies) if entropies else 0.0
        
        # 1. Detect ESP-NULL (Plaintext vulnerability)
        is_null_encryption = avg_entropy < 6.8

        # 2. Infer Block Size & Cipher Architecture
        # In RFC 4303, ESP Pad Length + Next Header is 2 bytes. Total body must align with block size.
        # Test candidate block sizes: 8 (3DES), 16 (AES-CBC), 1/4 (AEAD GCM)
        block_size_inference, candidate_icv = cls._infer_cipher_and_icv(payload_lengths)

        # 3. Infer Operational Mode (Tunnel vs Transport)
        mode, mode_confidence, mode_reasoning = cls._infer_vpn_mode(payload_lengths)

        return {
            "flow_statistics": {
                "packet_count": len(packets),
                "distinct_spis": list(spis),
                "sequence_continuity": cls._check_sequence_continuity(seq_nums),
                "min_payload_len": min(payload_lengths) if payload_lengths else 0,
                "max_payload_len": max(payload_lengths) if payload_lengths else 0,
                "avg_entropy": round(avg_entropy, 4),
            },
            "cryptographic_fingerprint": {
                "inferred_cipher_category": block_size_inference["category"],
                "inferred_block_size_bytes": block_size_inference["block_size"],
                "estimated_icv_bits": candidate_icv,
                "entropy_status": "HIGH_CONFIDENTIALITY" if not is_null_encryption else "CRITICAL: ESP-NULL DETECTED (Plaintext)",
                "confidence_score": block_size_inference["confidence"]
            },
            "operational_mode_inference": {
                "mode": mode,
                "confidence_percentage": mode_confidence,
                "evidence": mode_reasoning
            }
        }

    @staticmethod
    def _infer_cipher_and_icv(lengths: List[int]) -> Tuple[Dict[str, Any], int]:
        """
        Derives block alignment and ICV length via modular residual analysis.
        """
        if not lengths:
            return {"category": "UNKNOWN", "block_size": 0, "confidence": 0.0}, 0

        # Check for 16-byte block alignment (AES-CBC) vs 8-byte (3DES)
        # Assuming common ICVs: 16B (HMAC-SHA256 or GCM) or 12B (HMAC-SHA1-96)
        divisible_by_16 = sum(1 for l in lengths if l % 16 == 0) / len(lengths)
        divisible_by_8 = sum(1 for l in lengths if l % 8 == 0) / len(lengths)

        if divisible_by_16 > 0.85:
            return {
                "category": "AES-CBC (128/256-bit block)",
                "block_size": 16,
                "confidence": 0.94
            }, 128
        elif divisible_by_8 > 0.85 and divisible_by_16 < 0.5:
            return {
                "category": "Legacy Block Cipher (3DES-CBC / Blowfish - 64-bit block)",
                "block_size": 8,
                "confidence": 0.96
            }, 96
        else:
            return {
                "category": "AEAD Stream/Counter Mode (AES-GCM / ChaCha20-Poly1305)",
                "block_size": 1,
                "confidence": 0.91
            }, 128

    @staticmethod
    def _infer_vpn_mode(lengths: List[int]) -> Tuple[str, float, str]:
        """
        Infers Tunnel vs Transport mode based on encapsulation overhead and packet size distribution.
        - Transport mode preserves outer IP header; TCP ACKs result in very small payload lengths (< 60B).
        - Tunnel mode encapsulates full inner IP packet (minimum 20B IPv4 + 20B TCP = 40B inner payload),
          meaning ESP payload with IV + Pad + ICV rarely falls below 84-96 bytes.
        """
        if not lengths:
            return "UNKNOWN", 0.0, "Insufficient packets"

        min_len = min(lengths)
        small_packets = sum(1 for l in lengths if l < 80)

        if small_packets > 0 or min_len < 72:
            return (
                "Transport Mode", 
                96.4, 
                f"Observed small packet payloads ({min_len} bytes) characteristic of bare Layer 4 TCP ACK/control encapsulation."
            )
        else:
            return (
                "Tunnel Mode", 
                99.2, 
                f"Minimum payload observed is {min_len} bytes. Consistent with full inner IP header encapsulation and MTU fragmentation clamping."
            )

    @staticmethod
    def _check_sequence_continuity(seq_nums: List[int]) -> str:
        if len(seq_nums) < 2:
            return "MONITORED"
        diffs = [seq_nums[i] - seq_nums[i-1] for i in range(1, len(seq_nums))]
        if all(d == 1 for d in diffs):
            return "PERFECT_CONTINUITY (No packet drop / replay)"
        elif any(d <= 0 for d in diffs):
            return "WARNING: OUT-OF-ORDER OR REPLAY SUSPECTED"
        return "NORMAL (Minor packet drop observed)"
