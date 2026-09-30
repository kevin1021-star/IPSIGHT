"""
CIPHER-SENTINEL: Post-Quantum Threat & "Harvest Now, Decrypt Later" (HNDL) Engine
Quantifies cryptographic exposure to Cryptographically Relevant Quantum Computers (CRQCs)
operating under Shor's Algorithm and Grover's Search.
"""

from typing import Dict, Any, List

class PostQuantumThreatEngine:
    """
    Computes Quantum Threat Exposure Index (QTEI) and Confidentiality Half-Life.
    """

    @classmethod
    def evaluate_quantum_risk(cls, proposal: Dict[str, Any]) -> Dict[str, Any]:
        transforms = proposal.get("transforms", [])
        
        enc_t = next((t for t in transforms if t["type"] == "Encryption"), None)
        dh_t = next((t for t in transforms if t["type"] == "Diffie-Hellman"), None)
        
        dh_id = dh_t.get("id", 0) if dh_t else 0
        dh_bits = dh_t.get("bits", 0) if dh_t else 0
        enc_bits = enc_t.get("bits", 128) if enc_t else 128
        enc_name = enc_t.get("name", "") if enc_t else ""

        # 1. Classical Key Exchange Breakdown under Shor's Algorithm
        # Shor's algorithm solves discrete log and factoring in O((log N)^3)
        is_hybrid_pqc = dh_id == 1024 or "Kyber" in str(dh_t) or "ML-KEM" in str(dh_t)
        
        if is_hybrid_pqc:
            asymmetric_q_score = 0.0  # Fully Quantum Immune
            estimated_logical_qubits_to_break = "Immune to Known Quantum Algorithms (Lattice-based ML-KEM)"
            shor_vulnerable = False
            quantum_lifetime_years = "30+ Years (Post-Quantum Safe)"
        elif dh_id in [1, 2, 5]: # 768, 1024, 1536 bit MODP
            asymmetric_q_score = 1.0  # Already broken / zero margin
            estimated_logical_qubits_to_break = f"~{dh_bits * 2} Qubits (Within immediate near-term reach)"
            shor_vulnerable = True
            quantum_lifetime_years = "0 Years (CRITICAL: Immediate Decryption Threat)"
        elif dh_id in [14, 15, 16]: # 2048 - 4096 bit MODP
            asymmetric_q_score = 0.85
            estimated_logical_qubits_to_break = f"~{dh_bits * 2} Logical Qubits (Shor's Algorithm)"
            shor_vulnerable = True
            quantum_lifetime_years = "4 - 6 Years (HNDL Window: Active adversary interception)"
        elif dh_id in [19, 20, 21, 31, 32]: # ECC curves (P-256, P-384, Curve25519)
            asymmetric_q_score = 0.75
            # ECC requires fewer logical qubits to break than equivalent RSA! (~6n qubits)
            estimated_logical_qubits_to_break = f"~{dh_bits * 6} Logical Qubits (Proos-Zalka Shor adaptation)"
            shor_vulnerable = True
            quantum_lifetime_years = "5 - 7 Years (High HNDL Priority)"
        else:
            asymmetric_q_score = 0.9
            estimated_logical_qubits_to_break = "Unknown classical parameters"
            shor_vulnerable = True
            quantum_lifetime_years = "3 - 5 Years"

        # 2. Symmetric Cipher Breakdown under Grover's Algorithm
        # Grover reduces key search complexity from 2^k to 2^(k/2)
        effective_quantum_symmetric_bits = enc_bits // 2
        grover_safe = effective_quantum_symmetric_bits >= 128

        if enc_bits <= 64:
            symmetric_q_score = 1.0
            symmetric_assessment = f"CRITICAL: 64-bit key reduced to 2^{effective_quantum_symmetric_bits} search (Trivial quantum break)."
        elif enc_bits == 128:
            symmetric_q_score = 0.5
            symmetric_assessment = "MODERATE: 128-bit key reduced to 64-bit effective quantum security (NIST transition advised to AES-256)."
        else:
            symmetric_q_score = 0.0
            symmetric_assessment = "POST-QUANTUM RESISTANT: AES-256 maintains 128 bits of security against Grover's algorithm."

        # Aggregate Quantum Threat Exposure Index (QTEI): 0.0 (Safe) to 1.0 (Critical)
        qtei = round((asymmetric_q_score * 0.7) + (symmetric_q_score * 0.3), 3)

        return {
            "qtei_score": qtei,
            "threat_classification": "CRITICAL_QUANTUM_VULNERABLE" if qtei > 0.7 else "MODERATE_EXPOSURE" if qtei > 0.3 else "POST_QUANTUM_RESILIENT",
            "shor_algorithm_exposure": {
                "vulnerable": shor_vulnerable,
                "target_cipher": dh_t.get("name", "Unknown") if dh_t else "None",
                "estimated_logical_qubits_needed": estimated_logical_qubits_to_break,
                "hndl_risk_window": quantum_lifetime_years
            },
            "grover_algorithm_exposure": {
                "cipher_name": enc_name,
                "nominal_bits": enc_bits,
                "effective_quantum_bits": effective_quantum_symmetric_bits,
                "is_grover_resistant": grover_safe,
                "assessment": symmetric_assessment
            },
            "defense_action": "Migrate immediately to RFC 9370 Post-Quantum Hybrid (ML-KEM-768 + Curve25519) + AES-256-GCM." if qtei > 0.5 else "Compliant with forward-secrecy guidelines."
        }
