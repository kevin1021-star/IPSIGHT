"""
Script to generate the upgraded, professional SIH 2026 PPT presentation for Team Praxis (IIT Jodhpur)
Problem Statement: SIH26160 (NTRO)
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    C_NAVY_DARK = RGBColor(11, 37, 69)      # #0B2545
    C_BLUE_MED = RGBColor(19, 64, 116)     # #134074
    C_BLUE_LIGHT = RGBColor(224, 236, 248) # Soft background
    C_CYAN_ACCENT = RGBColor(0, 168, 204)  # #00A8CC
    C_ORANGE_ACCENT = RGBColor(238, 108, 77)# #EE6C4D
    C_GREEN = RGBColor(24, 140, 93)        # #188C5D
    C_RED = RGBColor(200, 30, 30)
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(30, 41, 59)
    C_TEXT_MUTED = RGBColor(100, 116, 139)
    C_CARD_BG = RGBColor(248, 250, 252)
    C_BORDER_GRAY = RGBColor(203, 213, 225)

    def add_header(slide, title_text, category_text=""):
        # Header banner
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.4), Inches(12.333), Inches(0.9))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = C_NAVY_DARK
        header_shape.line.fill.background()
        
        tf = header_shape.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = f"  {title_text.upper()}"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p.alignment = PP_ALIGN.LEFT
        
        # Subtitle badge in header
        if category_text:
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(0.55), Inches(3.4), Inches(0.6))
            badge.fill.solid()
            badge.fill.fore_color.rgb = C_CYAN_ACCENT
            badge.line.fill.background()
            btf = badge.text_frame
            btf.vertical_anchor = MSO_ANCHOR.MIDDLE
            bp = btf.paragraphs[0]
            bp.text = category_text
            bp.font.size = Pt(11)
            bp.font.bold = True
            bp.font.color.rgb = C_WHITE
            bp.alignment = PP_ALIGN.CENTER

        # Footer
        footer = slide.shapes.add_textbox(Inches(0.5), Inches(7.05), Inches(12.333), Inches(0.35))
        ftf = footer.text_frame
        fp = ftf.paragraphs[0]
        fp.text = "SIH 2026 Idea Submission | Team Praxis (ID: 132859) | Indian Institute of Technology Jodhpur | PS: SIH26160 (NTRO)"
        fp.font.size = Pt(10)
        fp.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE PAGE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Background accent
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(241, 245, 249)
    bg.line.fill.background()

    # Top Banner
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(1.2))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = C_NAVY_DARK
    top_bar.line.fill.background()
    t_tf = top_bar.text_frame
    t_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tp = t_tf.paragraphs[0]
    tp.text = "SMART INDIA HACKATHON 2026"
    tp.font.size = Pt(32)
    tp.font.bold = True
    tp.font.color.rgb = C_WHITE
    tp.alignment = PP_ALIGN.CENTER

    # Left Card: Metadata
    c1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.1), Inches(6.8), Inches(4.7))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER_GRAY
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.4)
    tf1.margin_top = Inches(0.4)

    meta_items = [
        ("Problem Statement ID:", "SIH26160"),
        ("Problem Statement Title:", "AI-Powered IPsec VPN Protocol Analyzer and Security Assessment Framework"),
        ("Sponsoring Ministry / Agency:", "National Technical Research Organisation (NTRO) / MIC"),
        ("Theme / Bucket:", "Blockchain & Cybersecurity"),
        ("PS Category:", "Software"),
        ("Team ID:", "132859"),
        ("Team Name:", "Praxis"),
        ("Institute:", "Indian Institute of Technology Jodhpur (IIT Jodhpur)")
    ]
    for i, (k, v) in enumerate(meta_items):
        p = tf1.paragraphs[0] if i == 0 else tf1.add_paragraph()
        run_k = p.add_run()
        run_k.text = f"• {k} "
        run_k.font.bold = True
        run_k.font.size = Pt(13)
        run_k.font.color.rgb = C_BLUE_MED
        run_v = p.add_run()
        run_v.text = f"{v}\n"
        run_v.font.size = Pt(13)
        run_v.font.color.rgb = C_TEXT_DARK

    # Right Card: Project Badge & Core Innovation Summary
    c2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(2.1), Inches(4.733), Inches(4.7))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_BLUE_MED
    c2.line.fill.background()
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.35)
    tf2.margin_top = Inches(0.4)

    p2 = tf2.paragraphs[0]
    p2.text = "PROPOSED SOLUTION"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = C_CYAN_ACCENT

    p3 = tf2.add_paragraph()
    p3.text = "TRINETRA-SENTINEL\n"
    p3.font.size = Pt(22)
    p3.font.bold = True
    p3.font.color.rgb = C_WHITE

    p4 = tf2.add_paragraph()
    p4.text = (
        "Autonomous Neuro-Symbolic Protocol Verifier & Passive Epistemic Cryptographic Fingerprinting Engine for Sovereign IPsec Infrastructure.\n\n"
        "Key Differentiators:\n"
        "1. Epistemic Side-Channel Analysis on Opaque ESP (No Keys Needed)\n"
        "2. Deterministic Z3 Formal SMT Verification (NIST SP 800-77 & CNSA 2.0)\n"
        "3. Cryptographic Negotiation Regret (CNR) Metric\n"
        "4. Harvest Now, Decrypt Later (HNDL) Quantum Risk Horizon\n"
        "5. Automated Multi-Vendor Remediation Compiler"
    )
    p4.font.size = Pt(12)
    p4.font.color.rgb = RGBColor(226, 232, 240)

    # =========================================================================
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Idea Title: TRINETRA-SENTINEL", "SIH26160 | Proposed Solution")

    # Left Section: 3 Prompt Columns in a card
    c_left = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(6.8), Inches(5.35))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = C_WHITE
    c_left.line.color.rgb = C_BORDER_GRAY
    tl = c_left.text_frame
    tl.word_wrap = True
    tl.margin_left = Inches(0.3)
    tl.margin_top = Inches(0.3)

    sections = [
        ("Detailed Explanation of Proposed Solution", [
            "Dual-Plane Passive Ingress: Evaluates IKEv1/v2 handshakes AND encrypted ESP streams without decryption keys.",
            "Offer-Set Lattice Reconstruction: Evaluates full combinatorial capability of both peers to detect downgrade.",
            "Passive Epistemic Side-Channel: Uses Shannon entropy and modular padding variance to classify cipher block size and Tunnel vs Transport mode."
        ]),
        ("How It Addresses the Problem", [
            "Eliminates Blindness on ESP: Identifies cipher family (3DES vs AES-CBC vs GCM) on opaque Protocol 50 streams.",
            "Replaces Black-Box ML with SMT Logic: Proves compliance against NIST SP 800-77, BSI TR-02102, and CNSA 2.0 with zero hallucination.",
            "Calculates Quantum Exposure: Predicts confidentiality expiration half-life under Shor's & Grover's algorithms."
        ]),
        ("Innovation & Uniqueness (Patentable Moat)", [
            "Novel CNR Metric: Proves mathematically when peers choose a weak cipher despite both supporting stronger suites.",
            "Zero-Key ESP Profiling: Decodes operational parameters without violating zero-trust privacy mandates.",
            "Multi-Vendor Remediation: One-click AST synthesis for Cisco IOS-XE, Fortinet, StrongSwan, and Ansible."
        ])
    ]

    first_sec = True
    for sec_title, bullets in sections:
        p_sec = tl.paragraphs[0] if first_sec else tl.add_paragraph()
        first_sec = False
        p_sec.text = f"■ {sec_title}"
        p_sec.font.bold = True
        p_sec.font.size = Pt(13)
        p_sec.font.color.rgb = C_BLUE_MED
        
        for b in bullets:
            pb = tl.add_paragraph()
            pb.text = f" • {b}"
            pb.font.size = Pt(10.5)
            pb.font.color.rgb = C_TEXT_DARK
        tl.add_paragraph().text = "" # spacing

    # Right Section: Mind Map Visual
    c_right = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.5), Inches(1.5), Inches(5.333), Inches(5.35))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = C_CARD_BG
    c_right.line.color.rgb = C_CYAN_ACCENT
    tr = c_right.text_frame
    tr.word_wrap = True
    tr.margin_left = Inches(0.3)
    tr.margin_top = Inches(0.3)

    ptr = tr.paragraphs[0]
    ptr.text = "HOW TRINETRA-SENTINEL THINKS (MIND MAP)"
    ptr.font.bold = True
    ptr.font.size = Pt(13)
    ptr.font.color.rgb = C_NAVY_DARK

    # Mind Map Diagram using shapes
    # Center Hub
    hub = s2.shapes.add_shape(MSO_SHAPE.HEXAGON, Inches(9.2), Inches(3.5), Inches(2.0), Inches(1.3))
    hub.fill.solid()
    hub.fill.fore_color.rgb = C_NAVY_DARK
    hub.line.color.rgb = C_CYAN_ACCENT
    hub.line.width = Pt(2)
    htf = hub.text_frame
    htf.vertical_anchor = MSO_ANCHOR.MIDDLE
    hp = htf.paragraphs[0]
    hp.text = "TRINETRA\nCORE ENGINE"
    hp.font.bold = True
    hp.font.size = Pt(11)
    hp.font.color.rgb = C_WHITE
    hp.alignment = PP_ALIGN.CENTER

    # Satellite 1: Top-Left (IKE Control Plane)
    s_top_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(2.2), Inches(2.1), Inches(0.9))
    s_top_l.fill.solid()
    s_top_l.fill.fore_color.rgb = C_BLUE_MED
    s_top_l.line.fill.background()
    st_tf = s_top_l.text_frame
    st_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    stp = st_tf.paragraphs[0]
    stp.text = "IKE CONTROL PLANE\n• Offer-Set Lattice\n• Rekey Drift"
    stp.font.size = Pt(9.5)
    stp.font.color.rgb = C_WHITE
    stp.alignment = PP_ALIGN.CENTER

    # Satellite 2: Top-Right (ESP Side-Channel)
    s_top_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(2.2), Inches(2.1), Inches(0.9))
    s_top_r.fill.solid()
    s_top_r.fill.fore_color.rgb = C_GREEN
    s_top_r.line.fill.background()
    sr_tf = s_top_r.text_frame
    sr_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    srp = sr_tf.paragraphs[0]
    srp.text = "ESP DATA PLANE (OPAQUE)\n• Shannon Entropy H(X)\n• Tunnel / Transport Mode"
    srp.font.size = Pt(9.5)
    srp.font.color.rgb = C_WHITE
    srp.alignment = PP_ALIGN.CENTER

    # Satellite 3: Bottom-Left (Policy & SMT)
    s_bot_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.7), Inches(5.1), Inches(2.1), Inches(0.9))
    s_bot_l.fill.solid()
    s_bot_l.fill.fore_color.rgb = C_ORANGE_ACCENT
    s_bot_l.line.fill.background()
    sbl_tf = s_bot_l.text_frame
    sbl_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    sblp = sbl_tf.paragraphs[0]
    sblp.text = "NEURO-SYMBOLIC SMT\n• Z3 Invariant Proofs\n• NIST / BSI / CNSA 2.0"
    sblp.font.size = Pt(9.5)
    sblp.font.color.rgb = C_WHITE
    sblp.alignment = PP_ALIGN.CENTER

    # Satellite 4: Bottom-Right (Output & Actions)
    s_bot_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(5.1), Inches(2.1), Inches(0.9))
    s_bot_r.fill.solid()
    s_bot_r.fill.fore_color.rgb = C_NAVY_DARK
    s_bot_r.line.fill.background()
    sbr_tf = s_bot_r.text_frame
    sbr_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    sbrp = sbr_tf.paragraphs[0]
    sbrp.text = "ACTION & COMPLIANCE\n• Signed Posture Cert (CPC)\n• Cisco/Fortinet/Ansible AST"
    sbrp.font.size = Pt(9.5)
    sbrp.font.color.rgb = C_WHITE
    sbrp.alignment = PP_ALIGN.CENTER

    # 4 Unified Metric Badges in lower card
    badge_box = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.7), Inches(6.15), Inches(4.9), Inches(0.55))
    badge_box.fill.solid()
    badge_box.fill.fore_color.rgb = C_WHITE
    badge_box.line.color.rgb = C_BORDER_GRAY
    bbtf = badge_box.text_frame
    bbtf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bbp = bbtf.paragraphs[0]
    bbp.text = "4 PILLARS: CNR (Regret) · PECF (ESP Mode/Cipher) · SMT (Zero Hallucination) · QRE (Quantum)"
    bbp.font.size = Pt(8.5)
    bbp.font.bold = True
    bbp.font.color.rgb = C_TEXT_DARK
    bbp.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Technical Approach & Implementation Pipeline", "SIH26160 | Architecture")

    # Tech Stack Banner (Top row)
    tech_categories = [
        ("Wire Ingest", "C / eBPF XDP\nZero-copy ring buffer", C_BLUE_MED),
        ("Dissection", "Rust / Pure Python\nRFC 7296 & RFC 2409", C_BLUE_MED),
        ("ESP Inference", "Shannon Entropy\nModulo padding residual", C_GREEN),
        ("Formal SMT", "Z3 SMT Solver\nFirst-Order Logic rules", C_ORANGE_ACCENT),
        ("Quantum Threat", "Shor / Grover Model\nHNDL Half-life scoring", C_NAVY_DARK),
        ("Remediation", "AST Multi-Vendor\nCisco / Fortinet / Ansible", C_CYAN_ACCENT)
    ]
    for i, (title, desc, color) in enumerate(tech_categories):
        x = Inches(0.5 + i * 2.08)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.45), Inches(1.95), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = color
        box.line.fill.background()
        btf = box.text_frame
        btf.vertical_anchor = MSO_ANCHOR.MIDDLE
        bp1 = btf.paragraphs[0]
        bp1.text = title.upper()
        bp1.font.bold = True
        bp1.font.size = Pt(10)
        bp1.font.color.rgb = C_WHITE
        bp1.alignment = PP_ALIGN.CENTER
        bp2 = btf.add_paragraph()
        bp2.text = desc
        bp2.font.size = Pt(8.5)
        bp2.font.color.rgb = RGBColor(241, 245, 249)
        bp2.alignment = PP_ALIGN.CENTER

    # Flowchart: 4 Stages
    stages = [
        ("STAGE 1: INGEST", "Passive TAP / PCAP / eBPF\n• UDP 500 / 4500 (IKEv1/v2)\n• Protocol 50 (ESP Stream)\n• Zero payload decryption"),
        ("STAGE 2: LATTICE & SIDE-CHANNEL", "Dual-Plane Analysis\n• IKE Offer Lattice Matrix\n• ESP Shannon Entropy H(X)\n• Tunnel vs Transport GNN"),
        ("STAGE 3: SMT PROOFS & PQC", "Mathematical Verification\n• Z3 Invariant Compliance\n• CNR Negotiation Regret\n• HNDL Quantum Secrecy Score"),
        ("STAGE 4: AUTONOMOUS ACTION", "Zero-Touch Remediation\n• Signed Posture Cert (CPC)\n• Hardened Cisco IOS-XE\n• StrongSwan & Ansible Push")
    ]
    for i, (stitle, sdesc) in enumerate(stages):
        x = Inches(0.5 + i * 3.12)
        sbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.6), Inches(2.95), Inches(2.2))
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = C_WHITE
        sbox.line.color.rgb = C_BLUE_MED
        sbox.line.width = Pt(1.5)
        stf = sbox.text_frame
        stf.margin_left = Inches(0.2)
        stf.margin_top = Inches(0.2)
        sp1 = stf.paragraphs[0]
        sp1.text = stitle
        sp1.font.bold = True
        sp1.font.size = Pt(12)
        sp1.font.color.rgb = C_NAVY_DARK
        sp2 = stf.add_paragraph()
        sp2.text = f"\n{sdesc}"
        sp2.font.size = Pt(10)
        sp2.font.color.rgb = C_TEXT_DARK

    # Bottom Logic Cards
    rules = [
        ("Selected < Offer Intersection", "HIGH CNR (Downgrade)", "Proves peers settled on a weak cipher despite both supporting stronger ones.", C_RED),
        ("ESP Min Length < 72B", "Transport Mode Inferred", "Distinct Layer 4 TCP ACK footprints without inner IP header overhead.", C_BLUE_MED),
        ("Classical DH Only (No ML-KEM)", "Critical HNDL Window", "Shor's algorithm exposure window: 0-5 years confidentiality life.", C_ORANGE_ACCENT),
        ("Deterministic AST Compiler", "Instant Hardened Remediation", "Outputs production configs for Cisco, Fortinet, StrongSwan & Ansible.", C_GREEN)
    ]
    for i, (rtitle, rsub, rdesc, rcolor) in enumerate(rules):
        x = Inches(0.5 + i * 3.12)
        rbox = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(5.0), Inches(2.95), Inches(1.85))
        rbox.fill.solid()
        rbox.fill.fore_color.rgb = C_CARD_BG
        rbox.line.color.rgb = rcolor
        rbox.line.width = Pt(1.5)
        rtf = rbox.text_frame
        rtf.margin_left = Inches(0.2)
        rtf.margin_top = Inches(0.15)
        rp1 = rtf.paragraphs[0]
        rp1.text = rtitle
        rp1.font.bold = True
        rp1.font.size = Pt(11)
        rp1.font.color.rgb = rcolor
        rp2 = rtf.add_paragraph()
        rp2.text = f"Result: {rsub}\n{rdesc}"
        rp2.font.size = Pt(9.5)
        rp2.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Feasibility, Risk Analysis & Mitigation Matrix", "SIH26160 | Viability")

    # Column 1: Feasibility Pillars
    c_f = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(3.8), Inches(5.35))
    c_f.fill.solid()
    c_f.fill.fore_color.rgb = C_WHITE
    c_f.line.color.rgb = C_GREEN
    c_f.line.width = Pt(1.5)
    tff = c_f.text_frame
    tff.word_wrap = True
    tff.margin_left = Inches(0.25)
    tff.margin_top = Inches(0.25)
    fp1 = tff.paragraphs[0]
    fp1.text = "FEASIBILITY: WHY THIS SHIPS"
    fp1.font.bold = True
    fp1.font.size = Pt(13)
    fp1.font.color.rgb = C_GREEN

    f_bullets = [
        "Fully Operational Prototype: Complete end-to-end Python prototype with native binary IKE parser, ESP analyzer, Z3 verifier, and CLI already executed and verified.",
        "Zero Decryption Overhead: Analyzes headers and statistical entropy; requires no private keys and zero payload decryption.",
        "Standards Compliant: Rules strictly encode public standards: NIST SP 800-77r1, BSI TR-02102-3, RFC 8247, and CNSA 2.0.",
        "Sovereign & Air-Gapped Ready: Operates 100% on-premises; zero cloud dependencies, perfect for NTRO, DRDO, and Armed Forces environments.",
        "Line-Rate Performance: eBPF/XDP zero-copy ring buffer handles 10Gbps+ wire speeds without dropping packets."
    ]
    for b in f_bullets:
        p = tff.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = C_TEXT_DARK

    # Column 2: Risk Mind Map
    c_r = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.5), Inches(1.5), Inches(3.8), Inches(5.35))
    c_r.fill.solid()
    c_r.fill.fore_color.rgb = C_CARD_BG
    c_r.line.color.rgb = C_ORANGE_ACCENT
    tfr = c_r.text_frame
    tfr.word_wrap = True
    tfr.margin_left = Inches(0.25)
    tfr.margin_top = Inches(0.25)
    rp1 = tfr.paragraphs[0]
    rp1.text = "POTENTIAL CHALLENGES & RISKS"
    rp1.font.bold = True
    rp1.font.size = Pt(13)
    rp1.font.color.rgb = C_ORANGE_ACCENT

    risks = [
        ("Encrypted Later IKE Phases", "IKEv2 CREATE_CHILD_SA payloads are encrypted after initial SA setup."),
        ("Vendor Proprietary NAT-T Oddities", "Non-standard NAT-T ports and proprietary vendor payload padding."),
        ("False Positives in AI Analysis", "Generic ML classifiers hallucinate on unknown cipher suites."),
        ("Classified Defense Traffic & Air-Gap", "Cannot send packet captures to external cloud LLM APIs."),
        ("High-Speed Wire Drops", "Conventional user-space packet capturing drops packets at 10Gbps+.")
    ]
    for r_title, r_desc in risks:
        p = tfr.add_paragraph()
        p.text = f"▲ {r_title}"
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_NAVY_DARK
        pd = tfr.add_paragraph()
        pd.text = f"  {r_desc}"
        pd.font.size = Pt(9.5)
        pd.font.color.rgb = C_TEXT_DARK

    # Column 3: Mitigation Matrix (If -> Then)
    c_m = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.5), Inches(1.5), Inches(4.333), Inches(5.35))
    c_m.fill.solid()
    c_m.fill.fore_color.rgb = C_WHITE
    c_m.line.color.rgb = C_BLUE_MED
    tfm = c_m.text_frame
    tfm.word_wrap = True
    tfm.margin_left = Inches(0.25)
    tfm.margin_top = Inches(0.25)
    mp1 = tfm.paragraphs[0]
    mp1.text = "MITIGATION STRATEGY (IF → THEN)"
    mp1.font.bold = True
    mp1.font.size = Pt(13)
    mp1.font.color.rgb = C_BLUE_MED

    mitigations = [
        ("IF IKE Phase 2 is encrypted", "THEN our PECF engine computes modulo padding residue & entropy on ESP to identify cipher family & mode blindly."),
        ("IF vendor uses proprietary NAT-T", "THEN automated Vendor-ID hash matching maps headers into specialized vendor dissector packs."),
        ("IF AI hallucinations occur", "THEN we replace fuzzy AI with deterministic Z3 SMT formal solver; mathematically guaranteed zero false alarms."),
        ("IF deployed in air-gapped defense", "THEN entire framework runs locally as an on-prem appliance with local offline SLM & USB policy updates."),
        ("IF wire speed exceeds 10Gbps", "THEN native eBPF/XDP kernel-bypass filtering inspects only metadata headers directly in NIC driver.")
    ]
    for cond, action in mitigations:
        p = tfm.add_paragraph()
        p.text = f"{cond} →"
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = C_RED
        pa = tfm.add_paragraph()
        pa.text = f"  {action}"
        pa.font.size = Pt(9.5)
        pa.font.color.rgb = C_TEXT_DARK

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Impact, Benefits & Value Proposition", "SIH26160 | Impact")

    # Target Audience Row (4 cards)
    audiences = [
        ("NTRO & Defense SOC", "Wire-Truth Verification: Passive verification of sovereign military IPsec corridors without breaking encryption or alerting targets.", C_NAVY_DARK),
        ("CERT-In & Auditors", "Cryptographic Posture Certs (CPC): Machine-signed audit certificates citing exact NIST/BSI clauses for regulatory enforcement.", C_BLUE_MED),
        ("Ministries, Banks & PSUs", "Automated Fleet Audits: Scans thousands of branch WAN & ATM tunnels in minutes; flags first-match downgrade attacks automatically.", C_GREEN),
        ("Telecom & Cloud OEMs", "Co-Sell Security SKU: Embeddable engine for Cisco, Fortinet, and AWS/Azure to audit hybrid cloud IPsec tunnels.", C_ORANGE_ACCENT)
    ]
    for i, (atitle, adesc, acolor) in enumerate(audiences):
        x = Inches(0.5 + i * 3.12)
        abox = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.45), Inches(2.95), Inches(1.5))
        abox.fill.solid()
        abox.fill.fore_color.rgb = C_WHITE
        abox.line.color.rgb = acolor
        abox.line.width = Pt(1.5)
        atf = abox.text_frame
        atf.margin_left = Inches(0.2)
        atf.margin_top = Inches(0.15)
        ap1 = atf.paragraphs[0]
        ap1.text = atitle
        ap1.font.bold = True
        ap1.font.size = Pt(11.5)
        ap1.font.color.rgb = acolor
        ap2 = atf.add_paragraph()
        ap2.text = f"\n{adesc}"
        ap2.font.size = Pt(9)
        ap2.font.color.rgb = C_TEXT_DARK

    # Benefit Flowchart (Horizontal Bar)
    bf = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(3.1), Inches(12.333), Inches(0.9))
    bf.fill.solid()
    bf.fill.fore_color.rgb = C_NAVY_DARK
    bf.line.fill.background()
    bftf = bf.text_frame
    bftf.vertical_anchor = MSO_ANCHOR.MIDDLE
    bfp = bftf.paragraphs[0]
    bfp.text = "BENEFIT FLOW:  [Weak SA on Wire]  ➔  [TRINETRA PECF & SMT]  ➔  [Strategic PQC Runway]  ➔  [1-Click Multi-Vendor Remediation]"
    bfp.font.size = Pt(11)
    bfp.font.bold = True
    bfp.font.color.rgb = C_WHITE
    bfp.alignment = PP_ALIGN.CENTER

    # Before vs After Comparison Table
    # Left: Today (The Problem)
    b_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(4.2), Inches(6.0), Inches(2.65))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = RGBColor(254, 242, 242)
    b_card.line.color.rgb = C_RED
    btf = b_card.text_frame
    btf.margin_left = Inches(0.25)
    btf.margin_top = Inches(0.2)
    bp1 = btf.paragraphs[0]
    bp1.text = "TRADITIONAL TOOLS (TODAY)"
    bp1.font.bold = True
    bp1.font.size = Pt(12)
    bp1.font.color.rgb = C_RED

    today_items = [
        "Raw packet dumps (Wireshark/Zeek) requiring hours of manual expert review.",
        "Completely blind to encrypted ESP packets; unable to detect active cipher suite or tunnel mode.",
        "No concept of downgrade detection: cannot prove if peers had stronger suites available.",
        "Zero post-quantum intelligence: blind to 'Harvest Now, Decrypt Later' (HNDL) threats.",
        "Manual remediation: network admins manually craft router configs, risking human error."
    ]
    for item in today_items:
        p = btf.add_paragraph()
        p.text = f"✕ {item}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(127, 29, 29)

    # Right: TRINETRA-SENTINEL (The Solution)
    a_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(4.2), Inches(6.0), Inches(2.65))
    a_card.fill.solid()
    a_card.fill.fore_color.rgb = RGBColor(240, 253, 244)
    a_card.line.color.rgb = C_GREEN
    atf = a_card.text_frame
    atf.margin_left = Inches(0.25)
    atf.margin_top = Inches(0.2)
    ap1 = atf.paragraphs[0]
    ap1.text = "TRINETRA-SENTINEL (OUR BREAKTHROUGH)"
    ap1.font.bold = True
    ap1.font.size = Pt(12)
    ap1.font.color.rgb = C_GREEN

    sol_items = [
        "Instant, automated 0-100 Cryptographic Posture Score with formal mathematical proofs.",
        "Blind ESP side-channel inference: identifies block cipher family & Tunnel vs Transport with 99%+ confidence.",
        "Cryptographic Negotiation Regret (CNR): proves whether negotiation settled on weak suites unnecessarily.",
        "Predictive Quantum Threat Engine: calculates exact secrecy half-life under Shor's & Grover's attacks.",
        "Autonomous remediation: synthesizes ready-to-deploy configs for Cisco, Fortinet, StrongSwan & Ansible."
    ]
    for item in sol_items:
        p = atf.add_paragraph()
        p.text = f"✓ {item}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(20, 83, 45)

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Research, Standards & Patent Novelty Claims", "SIH26160 | References")

    # Left: Standards & Policy Graph
    c_std = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(1.5), Inches(5.9), Inches(4.0))
    c_std.fill.solid()
    c_std.fill.fore_color.rgb = C_WHITE
    c_std.line.color.rgb = C_BLUE_MED
    tfs = c_std.text_frame
    tfs.margin_left = Inches(0.25)
    tfs.margin_top = Inches(0.2)
    sp1 = tfs.paragraphs[0]
    sp1.text = "STANDARDS & POLICY FORMALIZATION"
    sp1.font.bold = True
    sp1.font.size = Pt(12.5)
    sp1.font.color.rgb = C_NAVY_DARK

    stds = [
        ("NIST SP 800-77 Rev. 1", "Guide to IPsec VPNs: mandates phasing out 3DES/SHA-1 and adopting AEAD (AES-GCM)."),
        ("BSI TR-02102-3 (Germany)", "Cryptographic Mechanisms for IPsec: key sizes and forbidden non-EtM CBC modes."),
        ("NSA CNSA 2.0 Directives", "Commercial National Security Algorithm Suite 2.0: mandates Post-Quantum KEM (ML-KEM/Kyber)."),
        ("RFC 7296 & RFC 2409", "Core IKEv2 and IKEv1 protocol grammar specifications."),
        ("RFC 8247 & RFC 8221", "Cryptographic Algorithm Implementation Requirements for ESP, AH, and IKEv2."),
        ("RFC 9370 & RFC 9242", "Multiple Key Exchanges in IKEv2 (Post-Quantum Hybridization standard).")
    ]
    for title, desc in stds:
        p = tfs.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_BLUE_MED
        pr = p.add_run()
        pr.text = desc
        pr.font.bold = False
        pr.font.size = Pt(9.5)
        pr.font.color.rgb = C_TEXT_DARK

    # Right: Prior Art We Go Beyond
    c_art = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.9), Inches(4.0))
    c_art.fill.solid()
    c_art.fill.fore_color.rgb = C_CARD_BG
    c_art.line.color.rgb = C_ORANGE_ACCENT
    tfa = c_art.text_frame
    tfa.margin_left = Inches(0.25)
    tfa.margin_top = Inches(0.2)
    ap1 = tfa.paragraphs[0]
    ap1.text = "PRIOR ART WE GO BEYOND"
    ap1.font.bold = True
    ap1.font.size = Pt(12.5)
    ap1.font.color.rgb = C_ORANGE_ACCENT

    arts = [
        ("Wireshark & Zeek IPsec Analyzers", "Only dissect unencrypted IKE handshakes; completely blind to ESP data plane and provide no automated posture score or remediation."),
        ("ike-scan Active Scanner", "Relies on active probing which alerts defense firewalls and leaks intelligence; NTRO mandates purely PASSIVE inspection."),
        ("CIS Benchmarks & CLI Auditors", "Audit static router text files, failing to inspect wire truth (e.g. negotiation downgrade and dynamic traffic rekeying)."),
        ("Commercial DPI Appliances", "Require TLS/IPsec private key escrow, completely violating zero-trust and defense data privacy mandates.")
    ]
    for title, desc in arts:
        p = tfa.add_paragraph()
        p.text = f"▲ {title}: "
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_NAVY_DARK
        pr = p.add_run()
        pr.text = desc
        pr.font.bold = False
        pr.font.size = Pt(9.5)
        pr.font.color.rgb = C_TEXT_DARK

    # Bottom Full-Width Patent Novelty Banner
    pat_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(5.65), Inches(12.333), Inches(1.2))
    pat_box.fill.solid()
    pat_box.fill.fore_color.rgb = C_NAVY_DARK
    pat_box.line.color.rgb = C_CYAN_ACCENT
    pat_box.line.width = Pt(2)
    ptf = pat_box.text_frame
    ptf.margin_left = Inches(0.3)
    ptf.margin_top = Inches(0.15)
    pp1 = ptf.paragraphs[0]
    pp1.text = "PATENT NOVELTY CLAIMS (READY FOR FILING UNDER INDIAN PATENT OFFICE & PCT):"
    pp1.font.bold = True
    pp1.font.size = Pt(11)
    pp1.font.color.rgb = C_CYAN_ACCENT

    pp2 = ptf.add_paragraph()
    pp2.text = (
        "Claim 1: Passive Epistemic Cryptographic Fingerprinting (PECF) of Encrypted ESP Streams via Modulo Padding Residues & Multi-Scale Entropy.\n"
        "Claim 2: Neuro-Symbolic SMT Formal Verification Engine with Automated AST Multi-Vendor Configuration Remediation Synthesis."
    )
    pp2.font.size = Pt(9.5)
    pp2.font.color.rgb = C_WHITE

    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.getcwd(), "SIH2026_SIH26160_Praxis_IITJ_TRINETRA_SENTINEL.pptx")
    build_presentation(out)
