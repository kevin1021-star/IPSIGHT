"""
Script to precisely update the text in the provided SIH PPT template:
C:\\Users\\AS\\Downloads\\SIH26160_Praxis_TRINETRA_Idea_PPT.pptx
Preserves 100% of headers, footers, logos, shapes, colors, and layout.
Only elevates the text content inside the existing shapes.
"""

import pptx
import shutil
import os

def update_template_ppt(src_path: str, dst_path: str):
    # Copy original template first to preserve every byte of graphics, masters, layout
    shutil.copyfile(src_path, dst_path)
    prs = pptx.Presentation(dst_path)

    # -------------------------------------------------------------
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
    # -------------------------------------------------------------
    s2 = prs.slides[1]
    
    # Title banner shape [7]
    s2.shapes[7].text_frame.text = "TRINETRA-SENTINEL — Neuro-Symbolic & Epistemic Side-Channel IPsec Assessment Engine"
    s2.shapes[7].text_frame.paragraphs[0].font.bold = True

    # Shape [11]: Detailed explanation of the proposed solution
    tf_11 = s2.shapes[11].text_frame
    tf_11.clear()
    bullets_s2_1 = [
        "• Dual-plane passive ingress (PCAP/TAP/eBPF) — audits IKE & encrypted ESP streams without keys",
        "• Rebuilds FULL offer-set lattice to detect silent downgrade (selected SA vs intersection of offers)",
        "• Epistemic Side-Channel Engine: profiles ESP entropy & padding modulo to infer cipher & mode",
        "• Output: signed Cryptographic Posture Certificate (CPC) with RFC / NIST clause citations"
    ]
    for i, b in enumerate(bullets_s2_1):
        p = tf_11.paragraphs[0] if i == 0 else tf_11.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9.5)

    # Shape [14]: How it addresses the problem
    tf_14 = s2.shapes[14].text_frame
    tf_14.clear()
    bullets_s2_2 = [
        "• Solves ESP blindness: infers Tunnel vs Transport & cipher block size on raw Protocol 50 streams",
        "• Deterministic SMT logic flags weak DH 2/5, MD5/SHA-1, Sweet32 64-bit blocks & Aggressive Mode",
        "• Detects downgrade: flags when chosen SA < peer offer intersection (CNR regret metric)",
        "• Post-Quantum HNDL Engine: quantifies secrecy half-life against Shor's & Grover's algorithms"
    ]
    for i, b in enumerate(bullets_s2_2):
        p = tf_14.paragraphs[0] if i == 0 else tf_14.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9.5)

    # Shape [17]: Innovation and uniqueness of the solution
    tf_17 = s2.shapes[17].text_frame
    tf_17.clear()
    bullets_s2_3 = [
        "• Patent Wedge 1: Zero-Key ESP Epistemic Fingerprinting (entropy + padding residue = cipher/mode)",
        "• Patent Wedge 2: Offer-Lattice CNR + Neuro-Symbolic SMT verification (zero AI hallucination)",
        "• Quantum Secrecy Metric (QTEI): Shor/Grover vulnerability window for defense intelligence",
        "• Autonomous Multi-Vendor AST Compiler: outputs ready-to-deploy Cisco, Fortinet & StrongSwan configs"
    ]
    for i, b in enumerate(bullets_s2_3):
        p = tf_17.paragraphs[0] if i == 0 else tf_17.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9.5)

    # Mind Map Updates
    s2.shapes[20].text_frame.text = "TRINETRA\nSENTINEL"
    s2.shapes[22].text_frame.text = "DATA\nESP Side-Channel"
    s2.shapes[23].text_frame.text = "OUTPUT\nCPC + AST Patch"
    s2.shapes[24].text_frame.text = "POLICY\nNIST/BSI/CNSA"
    s2.shapes[25].text_frame.text = "4 METRICS\nCNR·PECF·SMT·QTEI"
    
    tf_26 = s2.shapes[26].text_frame
    tf_26.clear()
    p26 = tf_26.paragraphs[0]
    p26.text = "CNR  regret\nPECF  ESP cipher/mode\nSMT  zero-hallucination\nQTEI  quantum HNDL"
    p26.font.size = pptx.util.Pt(8)

    # -------------------------------------------------------------
    # SLIDE 3: TECHNICAL APPROACH
    # -------------------------------------------------------------
    s3 = prs.slides[2]
    
    # Top boxes:
    s3.shapes[9].text_frame.text = "eBPF + Rust/Py\nZero-copy IKE/ESP"
    s3.shapes[13].text_frame.text = "Z3 SMT Solver\nNeuro-Symbolic"
    s3.shapes[15].text_frame.text = "Air-gap AST\nLocal generator"

    # 4-stage pipeline:
    s3.shapes[22].text_frame.text = "SPAN / TAP / PCAP\nUDP 500 • 4500\nESP Protocol 50"
    s3.shapes[24].text_frame.text = "Rebuild Offer Lattice\nESP Entropy Profiling\nTunnel/Transport Mode"
    s3.shapes[26].text_frame.text = "Deterministic SMT Proofs\nIntersection vs Selected\nCNR • PECF • SMT • QTEI"
    s3.shapes[28].text_frame.text = "Explainable Z3 Verdict\nSigned CPC Cert\nCisco/Fortinet/Ansible AST"

    # Score logic bottom:
    s3.shapes[34].text_frame.text = "ESP Modulo Residue + Min Len → Mode & Cipher (PECF)"
    s3.shapes[36].text_frame.text = "Classical DH only, no ML-KEM → High QTEI (HNDL)"
    s3.shapes[37].text_frame.text = "Demo path: Live PCAPs (Legacy 3DES/MD5, ESP Opaque Stream, PQC Hybrid) → SMT Engine → Signed CPC → Multi-Vendor Patches"

    # -------------------------------------------------------------
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # -------------------------------------------------------------
    s4 = prs.slides[3]
    
    # Left Feasibility box [10]
    tf_4_10 = s4.shapes[10].text_frame
    tf_4_10.clear()
    feas_bullets = [
        "• Working Prototype Complete: zero-copy parser, ESP analyzer, Z3 verifier & CLI fully tested",
        "• Non-Invasive Passive Profiling: derives cipher & Tunnel/Transport mode with zero keys needed",
        "• Standards Compliant: mathematically encodes NIST SP 800-77r1, BSI TR-02102-3 & CNSA 2.0",
        "• 100% Air-Gapped Sovereign Ready: on-prem appliance, zero cloud exfiltration; fits NTRO directives",
        "• Line-Rate Scalability: eBPF/XDP zero-copy ring buffer handles 10Gbps+ without packet drops",
        "• We judge SELECTION & WIRE BEHAVIOR, not secrets"
    ]
    for i, b in enumerate(feas_bullets):
        p = tf_4_10.paragraphs[0] if i == 0 else tf_4_10.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9)

    # Overcome If -> Then
    s4.shapes[22].text_frame.text = "PECF analyzes ESP modulo padding & entropy to infer cipher & mode"
    s4.shapes[28].text_frame.text = "Deterministic Z3 SMT logic replaces fuzzy AI (zero false positives)"
    s4.shapes[34].text_frame.text = "eBPF/Rust kernel-bypass ingest; AST patch auto-deploys to routers"

    # -------------------------------------------------------------
    # SLIDE 5: IMPACT AND BENEFITS
    # -------------------------------------------------------------
    s5 = prs.slides[4]
    
    # Stakeholder descriptions
    s5.shapes[9].text_frame.text = "Wire-truth of national IPsec — not CLI screenshots; passive zero-touch audit"
    s5.shapes[11].text_frame.text = "Signed CPC with exact RFC / NIST / CNSA clause violation IDs"
    s5.shapes[13].text_frame.text = "Mesh heat-map: detects silent first-match downgrade across thousands of WAN tunnels"
    s5.shapes[15].text_frame.text = "Co-sell posture & migration SKU on existing Cisco, Fortinet & AWS gateways"

    # Benefit flow box [21]
    s5.shapes[21].text_frame.text = "Strategic\nPQC runway (QTEI)"

    # Before vs After
    tf_5_31 = s5.shapes[31].text_frame
    tf_5_31.clear()
    today_b = [
        "• Decode packets, no automated posture score",
        "• Flag MD5 as simple lookup table; blind to ESP mode & cipher",
        "• Config ≠ what the wire actually selected",
        "• Screenshot PDF for auditors; manual error-prone fixes"
    ]
    for i, b in enumerate(today_b):
        p = tf_5_31.paragraphs[0] if i == 0 else tf_5_31.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9)

    tf_5_34 = s5.shapes[34].text_frame
    tf_5_34.clear()
    trinetra_b = [
        "• Score negotiation regret (CNR) & infer ESP cipher/mode blindly",
        "• Deterministic SMT proofs of compliance (NIST / CNSA 2.0)",
        "• Harvest Now Decrypt Later (HNDL) quantum threat horizon",
        "• 1 handshake → 4 scores → 1 signed certificate → 1-click vendor fix"
    ]
    for i, b in enumerate(trinetra_b):
        p = tf_5_34.paragraphs[0] if i == 0 else tf_5_34.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(9)

    # -------------------------------------------------------------
    # SLIDE 6: RESEARCH AND REFERENCES
    # -------------------------------------------------------------
    s6 = prs.slides[5]
    
    # Standards box [10]
    tf_6_10 = s6.shapes[10].text_frame
    tf_6_10.clear()
    stds_b = [
        "• NIST SP 800-77 Rev.1 — IPsec VPN guide (deprecates 3DES/SHA-1)",
        "• BSI TR-02102-3 — IPsec crypto recommendations (prohibits non-EtM CBC)",
        "• NSA CNSA 2.0 — Post-Quantum KEM (ML-KEM / Kyber) mandates",
        "• RFC 7296 (IKEv2)    •    RFC 2409 (IKEv1)    •    RFC 4303 (ESP)",
        "• RFC 8247 / RFC 8221 — algorithm requirements",
        "• RFC 9370 & RFC 9242 — PQC hybrid key exchanges → our QTEI score",
        "• CERT-In cryptographic & sovereign VPN advisories",
        "csrc.nist.gov  •  datatracker.ietf.org  •  bsi.bund.de"
    ]
    for i, b in enumerate(stds_b):
        p = tf_6_10.paragraphs[0] if i == 0 else tf_6_10.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(8.5)

    # Prior art box [13]
    tf_6_13 = s6.shapes[13].text_frame
    tf_6_13.clear()
    prior_b = [
        "• Wireshark / Zeek IPsec — decode only; blind to ESP cipher/mode, no CNR",
        "• ike-scan — active probe; NTRO needs 100% PASSIVE inspection",
        "• VIAVI Avalanche — performance stress-test, not cryptographic posture",
        "• CIS / CLI auditors — inspect static configs, miss wire-level downgrade",
        "• Commercial DPI — requires private key escrow (violates Zero-Trust)",
        "zeek.org/2021/04/zeeks-ipsec-protocol-analyzer"
    ]
    for i, b in enumerate(prior_b):
        p = tf_6_13.paragraphs[0] if i == 0 else tf_6_13.add_paragraph()
        p.text = b
        p.font.size = pptx.util.Pt(8.5)

    # Novelty claim bottom banner [14]
    s6.shapes[14].text_frame.text = (
        "NOVELTY CLAIM • Dual-Plane Offer Lattice + ESP Epistemic Fingerprinting (PECF) + Neuro-Symbolic SMT + Post-Quantum HNDL + Signed CPC Certificate\n"
        "We do not decrypt tunnels. We prove whether the nation selected the strongest SA it had, passively infer ESP mode/ciphers without keys, and automate multi-vendor remediation."
    )
    s6.shapes[14].text_frame.paragraphs[0].font.size = pptx.util.Pt(9)
    if len(s6.shapes[14].text_frame.paragraphs) > 1:
        s6.shapes[14].text_frame.paragraphs[1].font.size = pptx.util.Pt(8)

    prs.save(dst_path)
    print(f"Upgraded presentation successfully saved to: {dst_path}")

if __name__ == "__main__":
    src = r"C:\Users\AS\Downloads\SIH26160_Praxis_TRINETRA_Idea_PPT.pptx"
    dst = r"C:\Users\AS\Downloads\vpn\SIH26160_Praxis_TRINETRA_UPGRADED_SUBMISSION.pptx"
    update_template_ppt(src, dst)
