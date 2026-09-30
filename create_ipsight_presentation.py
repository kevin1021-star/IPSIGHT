"""
IPsight SIH 2026 Presentation Generator
Problem Statement: SIH26160 (NTRO)
Theme: Blockchain & Cybersecurity
Strict adherence to SIH template guidelines, 6-page limit, and executive/technical aesthetic.
"""

import os
import sys
import shutil
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_ipsight_presentation():
    src_template = r"C:\Users\AS\Downloads\SIH2026-IDEA-Presentation-Format.pptx"
    output_pptx = r"C:\Users\AS\Downloads\vpn\IPsight_SIH26160_Submission.pptx"
    output_pdf = r"C:\Users\AS\Downloads\vpn\IPsight_SIH26160_Submission.pdf"

    shutil.copyfile(src_template, output_pptx)
    prs = pptx.Presentation(output_pptx)

    # Color Palette - Modern Cyber & Defense Theme
    C_NAVY_DARK = RGBColor(11, 37, 69)       # #0B2545
    C_NAVY_TITLE = RGBColor(15, 23, 42)      # #0F172A
    C_BLUE_MED = RGBColor(30, 58, 138)       # #1E3A8A
    C_BLUE_ACCENT = RGBColor(2, 132, 199)    # #0284C7
    C_CYAN_BG = RGBColor(240, 249, 255)      # #F0F9FF
    C_LIGHT_BG = RGBColor(248, 250, 252)     # #F8FAFC
    C_CARD_BORDER = RGBColor(226, 232, 240)  # #E2E8F0
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT_DARK = RGBColor(15, 23, 42)       # Slate 900
    C_TEXT_BODY = RGBColor(51, 65, 85)       # Slate 700
    C_TEXT_MUTED = RGBColor(100, 116, 139)   # Slate 500
    C_GREEN = RGBColor(16, 149, 94)          # Emerald Green #10955E
    C_GREEN_BG = RGBColor(236, 253, 245)     # Soft Green
    C_AMBER = RGBColor(217, 119, 6)          # Amber #D97706
    C_AMBER_BG = RGBColor(254, 243, 199)     # Soft Amber
    C_RED = RGBColor(220, 38, 38)            # Red #DC2626
    C_PURPLE = RGBColor(109, 40, 217)        # Violet #6D28D9

    def style_run(run, text, size=10.0, color=C_TEXT_BODY, bold=False, italic=False, font_name="Calibri"):
        run.text = text
        run.font.size = Pt(size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.italic = italic
        run.font.name = font_name

    def clear_textbox(shape):
        tf = shape.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = ""
        p_elements = list(tf._txBody.p_lst)
        for p_elem in p_elements[1:]:
            tf._txBody.remove(p_elem)

    def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_CARD_BORDER, border_width=1.0):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(border_width)
        else:
            shape.line.fill.background()
        return shape

    def update_oval_team(slide, team_text="Team\nPraxis"):
        for shape in slide.shapes:
            if shape.has_text_frame and "Your" in shape.text_frame.text and "Team" in shape.text_frame.text:
                clear_textbox(shape)
                tf = shape.text_frame
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                style_run(run, team_text, size=9.5, color=C_NAVY_DARK, bold=True)

    # -------------------------------------------------------------------------
    # SLIDE 1: TITLE PAGE
    # -------------------------------------------------------------------------
    s1 = prs.slides[0]
    # Update Slide 1 Left Metadata Box (Shape 5 / TextBox 9)
    s1_tb = None
    for shape in s1.shapes:
        if shape.has_text_frame and "Problem Statement ID" in shape.text_frame.text:
            s1_tb = shape
            break

    if s1_tb:
        clear_textbox(s1_tb)
        tf = s1_tb.text_frame
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Inches(0.1)
        tf.margin_bottom = Inches(0.1)
        
        meta_items = [
            ("Problem Statement ID:", " SIH26160"),
            ("Problem Statement Title:", " AI-Powered IPsec VPN Protocol Analyzer & Security Assessment Framework"),
            ("Project Codename:", " IPsight (Solution v2.0)"),
            ("Sponsoring Agency:", " National Technical Research Organisation (NTRO)"),
            ("Theme:", " Blockchain & Cybersecurity"),
            ("PS Category:", " Software"),
            ("Team ID:", " 132859"),
            ("Team Name:", " Praxis (Indian Institute of Technology Jodhpur)")
        ]
        
        for i, (label, val) in enumerate(meta_items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(4)
            p.space_before = Pt(2) if i > 0 else Pt(0)
            
            # Bullet symbol
            r_bullet = p.add_run()
            style_run(r_bullet, "• ", size=11.0, color=C_BLUE_ACCENT, bold=True)
            
            # Label
            r_lbl = p.add_run()
            style_run(r_lbl, label, size=11.0, color=C_NAVY_TITLE, bold=True)
            
            # Value
            r_val = p.add_run()
            style_run(r_val, val, size=10.5, color=C_TEXT_BODY, bold=(label in ["Problem Statement ID:", "Project Codename:", "Team Name:"]))

        # Add Team Composition Card on the Right of Slide 1
        s1_right = add_card(s1, 6.70, 1.35, 6.23, 4.35, bg_color=C_LIGHT_BG, border_color=C_BLUE_MED, border_width=1.5)
        rtf = s1_right.text_frame
        rtf.word_wrap = True
        rtf.margin_left = Inches(0.18)
        rtf.margin_right = Inches(0.18)
        rtf.margin_top = Inches(0.12)
        
        rp = rtf.paragraphs[0]
        rr = rp.add_run()
        style_run(rr, "TEAM PRAXIS — IIT JODHPUR (AISHE: U-0395)", size=11.0, color=C_BLUE_MED, bold=True)
        
        team_members = [
            ("Team Leader:", "Kumari Ankita", "B.Tech AI & Data Science (2nd Year)"),
            ("Team Member:", "Nandini Dhawan", "B.Tech AI & Data Science (2nd Year)"),
            ("Team Member:", "Chirag Jha", "B.Tech AI & Data Science (2nd Year)"),
            ("Team Member:", "Mayank Jangid", "B.Tech AI & Data Science (2nd Year)"),
            ("Team Member:", "Aayush", "B.Tech AI & Data Science (2nd Year)"),
            ("Team Member:", "Rudra Pratap Singh Chauhan", "B.Tech AI & Data Science (2nd Year)")
        ]
        for role, name, dept in team_members:
            p = rtf.add_paragraph()
            p.space_before = Pt(3)
            r1 = p.add_run()
            style_run(r1, f"• {role} ", size=8.5, color=C_NAVY_DARK, bold=True)
            r2 = p.add_run()
            style_run(r2, f"{name} ", size=8.5, color=C_BLUE_ACCENT, bold=True)
            r3 = p.add_run()
            style_run(r3, f"— {dept}", size=8.0, color=C_TEXT_MUTED, bold=False)

        # Add Core Principle Callout Banner at bottom of Slide 1
        callout = add_card(s1, 0.40, 5.85, 12.53, 0.95, bg_color=C_CYAN_BG, border_color=C_BLUE_ACCENT, border_width=1.5)
        ctf = callout.text_frame
        ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
        ctf.margin_left = Inches(0.2)
        ctf.margin_right = Inches(0.2)
        cp1 = ctf.paragraphs[0]
        cp1.alignment = PP_ALIGN.LEFT
        r_c1 = cp1.add_run()
        style_run(r_c1, "CORE ARCHITECTURAL PRINCIPLE: ", size=10.5, color=C_BLUE_MED, bold=True)
        r_c2 = cp1.add_run()
        style_run(r_c2, '"Directly observe what IPsec exposes; infer only what metadata supports; label every inference with confidence and evidence."', size=10.5, color=C_TEXT_DARK, bold=True, italic=True)
        
        cp2 = ctf.add_paragraph()
        cp2.space_before = Pt(3)
        r_c3 = cp2.add_run()
        style_run(r_c3, "100% Air-Gapped & Offline  |  Zero-Key Passive Inspection  |  Strict 3-Tier Evidence Provenance  |  Dual Security/Risk Scoring", size=9.5, color=C_TEXT_MUTED, bold=False)

    # -------------------------------------------------------------------------
    # SLIDE 2: IDEA TITLE & PROPOSED SOLUTION
    # -------------------------------------------------------------------------
    s2 = prs.slides[1]
    update_oval_team(s2)
    
    # Update Title
    for shape in s2.shapes:
        if shape.has_text_frame and "IDEA TITLE" in shape.text_frame.text:
            clear_textbox(shape)
            tf = shape.text_frame
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            style_run(r, "IPsight — AI-Powered IPsec VPN Protocol Analyzer & Security Assessment Framework", size=15.0, color=C_NAVY_TITLE, bold=True)

    # Remove default placeholder textbox in Slide 2
    for shape in list(s2.shapes):
        if shape.has_text_frame and "Proposed Solution (Describe your Idea" in shape.text_frame.text:
            shape.text_frame.text = ""

    # Add 3 Structured Content Columns / Cards for Slide 2
    card_w = 3.98
    card_h = 5.45
    top_pos = 1.30

    # Column 1: Detailed Explanation of Proposed Solution
    c1 = add_card(s2, 0.40, top_pos, card_w, card_h, bg_color=C_WHITE, border_color=C_BLUE_MED, border_width=1.5)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.18)
    tf1.margin_right = Inches(0.18)
    tf1.margin_top = Inches(0.15)
    
    p = tf1.paragraphs[0]
    r = p.add_run()
    style_run(r, "1. PROPOSED SOLUTION & WORKFLOW", size=11.5, color=C_BLUE_MED, bold=True)
    
    p = tf1.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    style_run(r, "IPsight is an offline-first IPsec assessment platform combining direct IKE/config protocol evidence with privacy-preserving ESP metadata inference.", size=9.5, color=C_TEXT_BODY, italic=True)

    points1 = [
        ("Automated Full Pipeline:", " Seamless testbed → capture → parse → infer → assess → report chain without manual intervention."),
        ("Strict 3-Tier Evidence Model:", " Direct (cleartext IKE/config), Inferred (ESP metadata with calibrated conf), Unknown (never guessed)."),
        ("M1 Auto Testbed Factory:", " Docker-Compose + strongSwan lab spinning up 12+ matrixed scenarios across ciphers, DH, PFS, and traffic types."),
        ("M2/M3 Deep Dissector:", " Non-intrusive stream parser for IKEv1/v2, ESP (proto 50), AH (proto 51) into normalized JSON with per-field provenance."),
        ("M4 AI Engine (5 Heads):", " Protocol ID, Mode ID, Crypto Profile, Calibrated Flow Classifier, Isolation Forest Anomaly Detection."),
        ("M5 Assessment & Reports:", " Deterministic YAML rules + bounded ML amplifiers generating Dual Scores & multi-vendor fixes.")
    ]
    for k, v in points1:
        p = tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k}", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, f" {v}", size=9.0, color=C_TEXT_BODY, bold=False)

    # Column 2: How it Addresses the Problem
    c2 = add_card(s2, 4.68, top_pos, card_w, card_h, bg_color=C_WHITE, border_color=C_BLUE_ACCENT, border_width=1.5)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.18)
    tf2.margin_right = Inches(0.18)
    tf2.margin_top = Inches(0.15)
    
    p = tf2.paragraphs[0]
    r = p.add_run()
    style_run(r, "2. HOW IT ADDRESSES THE PROBLEM", size=11.5, color=C_BLUE_ACCENT, bold=True)

    p = tf2.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    style_run(r, "Resolves critical audit latency, human error, encrypted blind spots, and lack of open ground-truth datasets.", size=9.5, color=C_TEXT_BODY, italic=True)

    points2 = [
        ("Sub-Minute Zero-Touch Audits:", " Replaces multi-day manual inspection; parses 100MB PCAP in <2 min and config files in <5 seconds."),
        ("Legacy & Exposure Detection:", " Flags IKEv1 Historic status, IKEv1 Aggressive Mode PSK leaks, 3DES/DES, MD5, and SHA-1 per RFC 8247 / NIST SP 800-77r1."),
        ("Silent Downgrade Identification:", " Detects when responder accepts the weakest offered transform despite client supporting modern AEAD."),
        ("Encrypted Traffic Visibility:", " Infers broad flow classes (VoIP, Web, Bulk, Video, ICMP) via packet timing/sizes with ZERO payload decryption."),
        ("Zero-Hallucination Remediation:", " Generates copy-paste configuration patches grounded in local RFC/NIST knowledge base for Cisco, Fortinet, and strongSwan."),
        ("Strict Air-Gap Security:", " Runs 100% offline with sandboxed workers; zero data, keys, or endpoints ever leave the host system.")
    ]
    for k, v in points2:
        p = tf2.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k}", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, f" {v}", size=9.0, color=C_TEXT_BODY, bold=False)

    # Column 3: Innovation and Uniqueness of the Solution
    c3 = add_card(s2, 8.96, top_pos, card_w, card_h, bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    tf3 = c3.text_frame
    tf3.word_wrap = True
    tf3.margin_left = Inches(0.18)
    tf3.margin_right = Inches(0.18)
    tf3.margin_top = Inches(0.15)
    
    p = tf3.paragraphs[0]
    r = p.add_run()
    style_run(r, "3. INNOVATION & UNIQUENESS", size=11.5, color=C_GREEN, bold=True)

    p = tf3.add_paragraph()
    p.space_before = Pt(4)
    r = p.add_run()
    style_run(r, "Pioneering evidence-first architecture that unifies deterministic compliance with calibrated machine intelligence.", size=9.5, color=C_TEXT_BODY, italic=True)

    points3 = [
        ("Evidence-Aware Inference:", " Outputs calibrated probabilities (Platt/Isotonic + Brier scores) with SHAP feature attribution (IAT periodicity, burstiness)."),
        ("Dual Security/Risk Scoring:", " Decoupled Posture Score (0–100, compliance) and Risk Score (0–100, threat urgency) + Threat Matrix (Likelihood × Impact)."),
        ("Automated Dataset Factory:", " Solves industry-wide IPsec dataset deficit by generating reproducible, fully-labeled ground truth by construction."),
        ("Vendor Fingerprint CVE Linkage:", " Extracts Vendor ID payloads to fingerprint gateway implementations and correlate relevant CVE vulnerabilities."),
        ("Tamper-Evident Report Verification:", " Every assessment generates a SHA-256 integrity hash with optional permissioned blockchain anchoring (Hyperledger Fabric)."),
        ("Post-Quantum Readiness:", " Evaluates classical DH vs RFC 9370 hybrid ML-KEM exchange paths aligned with CNSA 2.0 quantum transition timelines.")
    ]
    for k, v in points3:
        p = tf3.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k}", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, f" {v}", size=9.0, color=C_TEXT_BODY, bold=False)

    # -------------------------------------------------------------------------
    # SLIDE 3: TECHNICAL APPROACH
    # -------------------------------------------------------------------------
    s3 = prs.slides[2]
    update_oval_team(s3)
    
    # Remove default placeholder textbox in Slide 3
    for shape in list(s3.shapes):
        if shape.has_text_frame and "Technologies to be used" in shape.text_frame.text:
            shape.text_frame.text = ""

    # Top Half: 4-Stage Methodology Pipeline Cards
    s3_top = 1.25
    col_w = 2.95
    col_gap = 0.20
    
    stages = [
        ("STAGE 1: INGEST & SPLIT", C_BLUE_MED, [
            ("Sources:", "PCAP, Live TAP, strongSwan configs"),
            ("Stream Splitter:", "UDP 500/4500 (IKE), Proto 50 (ESP), Proto 51 (AH)"),
            ("Sessionizer:", "5-tuple + SPI flow tracking"),
            ("Throughput:", "100 MB PCAP parsed in <2 min")
        ]),
        ("STAGE 2: DEEP DISSECTION", C_BLUE_ACCENT, [
            ("IKE Dissection:", "Extract proposals, DH, Vendor IDs, NAT-T, DPD, Rekey timing"),
            ("ESP Inspection:", "SPI tracking, sequence jitter & ESN indicators"),
            ("Offer Lattice:", "Offered vs accepted proposal matrix"),
            ("Normalized Model:", "Structured JSON with provenance")
        ]),
        ("STAGE 3: AI INFERENCE", C_PURPLE, [
            ("H1 Protocol & H2 Mode:", "XGBoost structural & MTU headroom classifiers"),
            ("H3 Crypto Profile:", "Direct extraction / ESP size-distribution profile"),
            ("H4 Flow Classifier:", "IAT FFT periodicity (VoIP ~20ms, Video ~10-40ms)"),
            ("H5 Anomaly Engine:", "Isolation Forest on proposal rarity & SPI churn")
        ]),
        ("STAGE 4: ASSESS & REPORT", C_GREEN, [
            ("Rule Engine:", "YAML compliance pack (NIST, RFC 8247, CNSA 2.0)"),
            ("Dual Scoring:", "Security Posture (0-100) & Risk Score (0-100)"),
            ("Remediation:", "Cisco, Fortinet, strongSwan, Ansible"),
            ("Exports:", "ReportLab PDF, JSON, SARIF, SHA-256 Anchor")
        ])
    ]

    for idx, (st_title, st_color, st_items) in enumerate(stages):
        l_pos = 0.40 + idx * (col_w + col_gap)
        card = add_card(s3, l_pos, s3_top, col_w, 2.50, bg_color=C_WHITE, border_color=st_color, border_width=1.5)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.12)
        ctf.margin_right = Inches(0.12)
        ctf.margin_top = Inches(0.10)
        
        p = ctf.paragraphs[0]
        r = p.add_run()
        style_run(r, st_title, size=10.5, color=st_color, bold=True)
        
        for k, v in st_items:
            p = ctf.add_paragraph()
            p.space_before = Pt(3)
            r1 = p.add_run()
            style_run(r1, f"• {k} ", size=8.5, color=C_NAVY_DARK, bold=True)
            r2 = p.add_run()
            style_run(r2, v, size=8.5, color=C_TEXT_BODY, bold=False)

    # Bottom Half: Technical Stack & 3-Tier Evidence Matrix
    s3_bot_top = 3.90
    
    # Bottom Left: Tech Stack Table / Card (Width: 5.8)
    b_left = add_card(s3, 0.40, s3_bot_top, 5.95, 2.85, bg_color=C_LIGHT_BG, border_color=C_BLUE_MED, border_width=1.5)
    btf1 = b_left.text_frame
    btf1.word_wrap = True
    btf1.margin_left = Inches(0.15)
    btf1.margin_right = Inches(0.15)
    btf1.margin_top = Inches(0.10)
    
    p = btf1.paragraphs[0]
    r = p.add_run()
    style_run(r, "TECHNOLOGIES & ARCHITECTURAL STACK", size=11.0, color=C_BLUE_MED, bold=True)
    
    tech_stack = [
        ("Packet Dissection:", " Python 3.11+, Scapy, tshark/dpkt, eBPF stream splitters"),
        ("AI / ML Engine:", " scikit-learn, XGBoost, Isolation Forest, SHAP, Platt Calibration"),
        ("Testbed Factory:", " Docker-Compose, strongSwan 5.9+, iperf3, SIPp (VoIP), ffmpeg RTP"),
        ("Backend & KB:", " FastAPI, SQLite / PostgreSQL, Local Vector DB (RFC/NIST RAG)"),
        ("Frontend & Visuals:", " React 18, Vite, TailwindCSS, Recharts, Lucide Icons"),
        ("Audit & Integrity:", " ReportLab PDF Engine, SARIF exporter, SHA-256 Ledger Anchor")
    ]
    for k, v in tech_stack:
        p = btf1.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        style_run(r1, f"• {k}", size=8.5, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=8.5, color=C_TEXT_BODY, bold=False)

    # Bottom Right: 3-Tier Evidence Taxonomy Card (Width: 6.3)
    b_right = add_card(s3, 6.55, s3_bot_top, 6.38, 2.85, bg_color=C_LIGHT_BG, border_color=C_GREEN, border_width=1.5)
    btf2 = b_right.text_frame
    btf2.word_wrap = True
    btf2.margin_left = Inches(0.15)
    btf2.margin_right = Inches(0.15)
    btf2.margin_top = Inches(0.10)
    
    p = btf2.paragraphs[0]
    r = p.add_run()
    style_run(r, "EVIDENCE-FIRST TAXONOMY (TRUTH VS INFERENCE)", size=11.0, color=C_GREEN, bold=True)

    evidence_rows = [
        ("DIRECT (High Conf):", " IKE version, offered/accepted ciphers, DH group, Vendor ID, NAT-T, DPD, NULL ESP — extracted verbatim from cleartext IKE/configs."),
        ("INFERRED (Calibrated):", " Flow traffic category (VoIP/Web/Bulk/Video), ESP-only cryptographic profile, mode indicators — derived from packet size/IAT metadata."),
        ("UNKNOWN (Never Guessed):", " Post-INIT IKEv2 secrets, CHILD_SA PFS (without rekey evidence), Pre-Shared Key strings — strictly flagged as Unknown to prevent false claims.")
    ]
    for k, v in evidence_rows:
        p = btf2.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        style_run(r1, f"• {k}", size=8.5, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=8.5, color=C_TEXT_BODY, bold=False)

    p = btf2.add_paragraph()
    p.space_before = Pt(4)
    r_sum = p.add_run()
    style_run(r_sum, "Key Fact: IKEv2 encrypts everything after IKE_SA_INIT. IPsight respects cryptographic reality: payload is never decrypted; ML never produces findings alone.", size=8.0, color=C_BLUE_MED, italic=True)

    # -------------------------------------------------------------------------
    # SLIDE 4: FEASIBILITY AND VIABILITY
    # -------------------------------------------------------------------------
    s4 = prs.slides[3]
    update_oval_team(s4)
    
    # Remove default placeholder textbox in Slide 4
    for shape in list(s4.shapes):
        if shape.has_text_frame and "Analysis of the feasibility of the idea" in shape.text_frame.text:
            shape.text_frame.text = ""

    s4_top = 1.25
    
    # Left Card: Feasibility & Viability Analysis (Width: 5.60)
    s4_left = add_card(s4, 0.40, s4_top, 5.60, 5.50, bg_color=C_WHITE, border_color=C_BLUE_MED, border_width=1.5)
    s4_tf1 = s4_left.text_frame
    s4_tf1.word_wrap = True
    s4_tf1.margin_left = Inches(0.18)
    s4_tf1.margin_right = Inches(0.18)
    s4_tf1.margin_top = Inches(0.15)
    
    p = s4_tf1.paragraphs[0]
    r = p.add_run()
    style_run(r, "FEASIBILITY & VIABILITY ANALYSIS", size=11.5, color=C_BLUE_MED, bold=True)
    
    feas_points = [
        ("Technical Feasibility (High):", " Built on validated open-source networking and ML primitives (Scapy, XGBoost, Isolation Forest). Lightweight footprint runs on standard commodity x86/ARM hardware without GPU dependencies."),
        ("Operational Feasibility (High):", " Memory-bounded streaming architecture processes large enterprise PCAPs efficiently (<2 min for 100MB PCAP; <5 sec for router configs). Ideal for edge appliances."),
        ("National Security Air-Gap Ready:", " 100% offline deployment with zero internet connectivity requirements; sandboxed parsers isolate untrusted PCAP inputs to prevent exploit execution."),
        ("Standards & Regulatory Compliance:", " Directly operationalizes authoritative NIST SP 800-77 Rev. 1, NIST SP 800-131A, BSI TR-02102-3, RFC 8247, RFC 8221, and NSA CNSA 2.0 criteria."),
        ("Multi-Vendor Interoperability:", " Modular dissector packs support Cisco IOS-XE, Fortinet FortiOS, strongSwan, Libreswan, and cloud VPN gateways (AWS/Azure)."),
        ("Dual-Plane Viability:", " Eliminates operational pushback by providing 100% passive monitoring with ZERO router performance impact and zero gateway credential requirements.")
    ]
    for k, v in feas_points:
        p = s4_tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k} ", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=9.0, color=C_TEXT_BODY, bold=False)

    # Right Card: Potential Challenges, Risks & Mitigation Strategies (Width: 6.75)
    s4_right = add_card(s4, 6.20, s4_top, 6.73, 5.50, bg_color=C_WHITE, border_color=C_AMBER, border_width=1.5)
    s4_tf2 = s4_right.text_frame
    s4_tf2.word_wrap = True
    s4_tf2.margin_left = Inches(0.18)
    s4_tf2.margin_right = Inches(0.18)
    s4_tf2.margin_top = Inches(0.15)
    
    p = s4_tf2.paragraphs[0]
    r = p.add_run()
    style_run(r, "CHALLENGES, RISKS & MITIGATION MATRIX", size=11.5, color=C_AMBER, bold=True)

    challenges = [
        ("Risk 1: No Open Labelled IPsec Datasets", 
         "M1 Auto Testbed acts as a synthetic dataset factory, generating 12+ matrixed ground-truth scenarios (ciphers × DH × PFS × traffic types)."),
        ("Risk 2: Encrypted ESP Opacity (Zero-Key)", 
         "Strict 3-Tier Evidence Taxonomy. Directly extract IKE parameters; estimate broad ESP traffic profiles probabilistically; never overclaim cipher recovery."),
        ("Risk 3: Metadata Shaping & Padding Evasion", 
         "Isotonic/Platt calibration reports explicit Brier confidence scores; ML findings act only as bounded amplifiers, while security score remains anchored on direct rules."),
        ("Risk 4: LLM Hallucination / Overclaiming", 
         "Zero LLM guessing in the core pipeline; deterministic YAML rule packs + local RAG vector DB over official RFC/NIST text for citations."),
        ("Risk 5: Untrusted PCAP Memory Corruption", 
         "Isolated sandbox worker processes with bounded CPU/RAM execution quotas and strict fuzzing-hardened Scapy/dpkt parsers."),
        ("Risk 6: Heterogeneous Vendor Syntax", 
         "AST-based template engine auto-generates exact vendor-native remediation scripts (Cisco CLI, FortiOS CLI, strongSwan swanctl.conf, Ansible).")
    ]
    for ch, mit in challenges:
        p = s4_tf2.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        style_run(r1, f"▲ {ch}: ", size=8.5, color=C_RED, bold=True)
        r2 = p.add_run()
        style_run(r2, mit, size=8.5, color=C_TEXT_BODY, bold=False)

    # -------------------------------------------------------------------------
    # SLIDE 5: IMPACT AND BENEFITS
    # -------------------------------------------------------------------------
    s5 = prs.slides[4]
    update_oval_team(s5)
    
    # Remove default placeholder textbox in Slide 5
    for shape in list(s5.shapes):
        if shape.has_text_frame and "Potential impact on the target audience" in shape.text_frame.text:
            shape.text_frame.text = ""

    s5_top = 1.25
    
    # Left Box: Impact on Target Audience (Stakeholders) (Width: 5.95)
    s5_left = add_card(s5, 0.40, s5_top, 5.95, 5.50, bg_color=C_WHITE, border_color=C_BLUE_MED, border_width=1.5)
    s5_tf1 = s5_left.text_frame
    s5_tf1.word_wrap = True
    s5_tf1.margin_left = Inches(0.18)
    s5_tf1.margin_right = Inches(0.18)
    s5_tf1.margin_top = Inches(0.15)
    
    p = s5_tf1.paragraphs[0]
    r = p.add_run()
    style_run(r, "TARGET AUDIENCE IMPACT", size=11.5, color=C_BLUE_MED, bold=True)

    stakeholders = [
        ("NTRO / Defense / National Cyber Command:", " Non-intrusive, passive wire-truth audit of sovereign VPN networks. Detects covert downgrade attacks and crypto decay without requiring endpoint private keys or credentials."),
        ("CERT-In & Sovereign Regulatory Auditors:", " Automates national IPsec compliance inspections with standardized RFC/NIST clause citations and tamper-evident SHA-256 cryptographic reports."),
        ("Critical Telecom & Service Providers:", " Audits multi-tenant IPsec gateways across thousands of enterprise WAN tunnels in seconds, highlighting high-risk configurations in real-time."),
        ("Enterprise SOC & Incident Responders:", " Provides continuous encrypted traffic behavioral visibility (identifying anomalous bulk exfiltration or covert channels inside ESP tunnels)."),
        ("Network Administrators & SecOps:", " Converts complex cryptographic findings into instant, 1-click vendor remediation commands (Cisco, Fortinet, strongSwan), eliminating human error.")
    ]
    for k, v in stakeholders:
        p = s5_tf1.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k} ", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=9.0, color=C_TEXT_BODY, bold=False)

    # Right Box: Strategic, Social, Economic & Security Benefits (Width: 6.38)
    s5_right = add_card(s5, 6.55, s5_top, 6.38, 5.50, bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    s5_tf2 = s5_right.text_frame
    s5_tf2.word_wrap = True
    s5_tf2.margin_left = Inches(0.18)
    s5_tf2.margin_right = Inches(0.18)
    s5_tf2.margin_top = Inches(0.15)
    
    p = s5_tf2.paragraphs[0]
    r = p.add_run()
    style_run(r, "QUANTIFIABLE BENEFITS & STRATEGIC VALUE", size=11.5, color=C_GREEN, bold=True)

    benefits = [
        ("Security Hardening & Zero-Blindspots:", " Uncovers hidden legacy suites (3DES, MD5, SHA-1, DH <14), IKEv1 Aggressive Mode PSK leaks, and responder downgrade vulnerabilities before attackers exploit them."),
        ("90%+ Operational Cost & Time Savings:", " Reduces audit cycles from 3–5 manual engineering days to <2 minutes per gateway, freeing up high-tier security analysts for active defense."),
        ("Privacy-Preserving Behavioral Intelligence:", " Delivers flow classification (VoIP, Web, Video, Bulk) and anomaly detection purely from metadata without decrypting or storing user payloads."),
        ("Post-Quantum Readiness (PQC Runway):", " Evaluates classical DH groups against RFC 9370 hybrid ML-KEM pathways, mitigating Harvest Now Decrypt Later (HNDL) quantum threats."),
        ("Zero Proprietary Lock-In / Open Standard:", " Built entirely on open-source standards; containerized deployment with zero cloud egress or expensive hardware licensing fees."),
        ("Tamper-Proof Audit Integrity:", " Cryptographic SHA-256 fingerprinting ensures audit reports are mathematically verifiable for compliance filings and court evidence.")
    ]
    for k, v in benefits:
        p = s5_tf2.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        style_run(r1, f"• {k} ", size=9.0, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=9.0, color=C_TEXT_BODY, bold=False)

    # -------------------------------------------------------------------------
    # SLIDE 6: RESEARCH AND REFERENCES
    # -------------------------------------------------------------------------
    s6 = prs.slides[5]
    update_oval_team(s6)
    
    # Remove default placeholder textbox in Slide 6
    for shape in list(s6.shapes):
        if shape.has_text_frame and "Details / Links of the reference" in shape.text_frame.text:
            shape.text_frame.text = ""

    s6_top = 1.25
    
    # Left Card: Authoritative Standards & RFC Specifications (Width: 5.95)
    s6_left = add_card(s6, 0.40, s6_top, 5.95, 4.10, bg_color=C_WHITE, border_color=C_BLUE_MED, border_width=1.5)
    s6_tf1 = s6_left.text_frame
    s6_tf1.word_wrap = True
    s6_tf1.margin_left = Inches(0.18)
    s6_tf1.margin_right = Inches(0.18)
    s6_tf1.margin_top = Inches(0.12)
    
    p = s6_tf1.paragraphs[0]
    r = p.add_run()
    style_run(r, "AUTHORITATIVE STANDARDS & SPECIFICATIONS", size=11.0, color=C_BLUE_MED, bold=True)

    rfc_refs = [
        ("RFC 7296 / RFC 4301 / RFC 4303:", " Internet Key Exchange Protocol Version 2 (IKEv2), Security Architecture for IP, and IP Encapsulating Security Payload (ESP)."),
        ("RFC 8247 & RFC 8221 (Current):", " Cryptographic Algorithm Implementation Requirements for IKEv2 and ESP/AH (IETF deprecation of 3DES, DES, MD5, SHA-1)."),
        ("IETF draft-ietf-ipsecme-ikev1-to-historic:", " Formal transition of IKEv1 to Historic status due to structural weaknesses."),
        ("RFC 9370 & RFC 9242:", " Multiple Key Exchanges in IKEv2 for Post-Quantum Hybrid Cryptography (ML-KEM / Kyber transition)."),
        ("NIST SP 800-77 Rev. 1 & NIST SP 800-131A:", " Guide to IPsec VPNs & Transitions: mandates IKEv2, DH groups ≥14 (2048-bit), and AES-GCM / SHA-256."),
        ("NSA CNSA 2.0 & BSI TR-02102-3:", " National Post-Quantum Migration timelines & Cryptographic Mechanisms for IPsec.")
    ]
    for k, v in rfc_refs:
        p = s6_tf1.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        style_run(r1, f"• {k} ", size=8.5, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=8.5, color=C_TEXT_BODY, bold=False)

    # Right Card: Academic Literature, ML Foundations & Prior Art (Width: 6.38)
    s6_right = add_card(s6, 6.55, s6_top, 6.38, 4.10, bg_color=C_WHITE, border_color=C_GREEN, border_width=1.5)
    s6_tf2 = s6_right.text_frame
    s6_tf2.word_wrap = True
    s6_tf2.margin_left = Inches(0.18)
    s6_tf2.margin_right = Inches(0.18)
    s6_tf2.margin_top = Inches(0.12)
    
    p = s6_tf2.paragraphs[0]
    r = p.add_run()
    style_run(r, "ACADEMIC FOUNDATIONS & PRIOR ART BENCHMARKS", size=11.0, color=C_GREEN, bold=True)

    acad_refs = [
        ("Lundberg & Lee (2017) — SHAP Explainability:", " Unified approach to interpreting model predictions for flow feature attribution (IAT periodicity, packet burstiness)."),
        ("Liu, Ting, Zhou (2008) — Isolation Forest:", " High-dimensional outlier isolation for detecting abnormal proposal distributions and sequence anomalies."),
        ("Guo et al. (2017) — Model Calibration:", " Isotonic regression & Platt scaling to guarantee well-calibrated confidence and Brier reliability."),
        ("Wireshark & Zeek IPsec Dissectors:", " Protocol dissection benchmark; IPsight extends with automated scoring, provenance tags, and flow intelligence."),
        ("ike-scan & Nessus IPsec Plugins:", " Active probing tools; IPsight is designed for 100% PASSIVE wire-truth assessment and automated vendor remediation.")
    ]
    for k, v in acad_refs:
        p = s6_tf2.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        style_run(r1, f"• {k} ", size=8.5, color=C_NAVY_DARK, bold=True)
        r2 = p.add_run()
        style_run(r2, v, size=8.5, color=C_TEXT_BODY, bold=False)

    # Bottom Full-Width Banner: Novelty Claim & Deliverables Pack
    s6_banner = add_card(s6, 0.40, 5.45, 12.53, 1.35, bg_color=C_CYAN_BG, border_color=C_BLUE_ACCENT, border_width=1.5)
    s6_btf = s6_banner.text_frame
    s6_btf.word_wrap = True
    s6_btf.margin_left = Inches(0.18)
    s6_btf.margin_right = Inches(0.18)
    s6_btf.margin_top = Inches(0.10)
    
    p = s6_btf.paragraphs[0]
    r1 = p.add_run()
    style_run(r1, "CORE NOVELTY CLAIM & DELIVERABLES STATUS: ", size=10.0, color=C_BLUE_MED, bold=True)
    r2 = p.add_run()
    style_run(r2, "IPsight does not break or decrypt tunnels. It proves whether the wire selected the strongest cryptographic suite, isolates downgrade risks, infers traffic metadata with calibrated confidence, and auto-generates multi-vendor fixes.", size=9.5, color=C_TEXT_DARK, bold=True)

    p2 = s6_btf.add_paragraph()
    p2.space_before = Pt(3)
    r3 = p2.add_run()
    style_run(r3, "✓ M1 Auto Testbed Factory (12 Scenarios)  |  ✓ 5-Head Calibrated AI Engine  |  ✓ FastAPI Backend + React Dashboard  |  ✓ Technical & Executive Reports", size=9.0, color=C_GREEN, bold=True)

    # -------------------------------------------------------------------------
    # DELETE SLIDE 7 (Instruction Slide)
    # -------------------------------------------------------------------------
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]
        print(f"Slide 7 (Instruction slide) successfully removed. Total slides remaining: {len(prs.slides)}")

    prs.save(output_pptx)
    print(f"Presentation saved successfully to: {output_pptx}")

    # Convert PPTX to PDF using PowerPoint COM
    try:
        import comtypes.client
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1
        deck = powerpoint.Presentations.Open(os.path.abspath(output_pptx))
        deck.SaveAs(os.path.abspath(output_pdf), 32) # 32 = ppSaveAsPDF
        deck.Close()
        powerpoint.Quit()
        print(f"PDF saved successfully to: {output_pdf}")
    except Exception as e:
        print(f"COM PDF conversion notice: {e}")

if __name__ == "__main__":
    create_ipsight_presentation()
