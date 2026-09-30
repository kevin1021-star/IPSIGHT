"""
Generate a Perfectly Proportioned Hand-Made / Blueprint Slide Graphic for Slide 3
Sits seamlessly beneath the official SIH slide header 'TECHNICAL APPROACH'.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import pptx
from pptx.util import Inches

out_dir = r"C:\Users\AS\Downloads\vpn"
art_dir = r"C:\Users\AS\.gemini\antigravity\brain\eb8c9836-bba9-4526-a239-b44851c8fe47"
pptx_path = os.path.join(out_dir, "IPsight_SIH26160_Submission.pptx")
pdf_path = os.path.join(out_dir, "IPsight_SIH26160_Submission.pdf")
mirror_pptx = r"C:\Users\AS\Downloads\SIH2026_IDEA_IPsight_Praxis.pptx"
mirror_pdf = r"C:\Users\AS\Downloads\SIH2026_IDEA_IPsight_Praxis.pdf"

def create_crisp_handmade_slide():
    # 16:9 ratio canvas matching the slide content area exactly
    fig, ax = plt.subplots(figsize=(16, 7.2), dpi=250)
    
    BG_COLOR = "#FFFFFF"       # Match PPT background perfectly
    INK_DARK = "#0F172A"       # Slate 900
    INK_BLUE = "#1D4ED8"       # Blue 700
    INK_PURPLE = "#6D28D9"     # Violet 700
    INK_AMBER = "#D97706"      # Amber 600
    INK_GREEN = "#059669"      # Emerald 600
    INK_RED = "#DC2626"        # Red 600
    CARD_BG = "#FFFFFF"
    CARD_LIGHT = "#F8FAFC"
    
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7.2)
    ax.axis('off')

    # 4 Main Pipeline Stages (Top Row)
    stages = [
        ("STAGE 1: INGEST", INK_BLUE, [
            ("Input Feeds:", "PCAP, Live Tap, Config files"),
            ("Stream Splitter:", "UDP 500/4500 (IKE) vs ESP/AH"),
            ("Sessionizer:", "5-Tuple + SPI flow tracking"),
            ("Throughput:", "⚡ 100MB PCAP in <2 minutes")
        ]),
        ("STAGE 2: DISSECT", INK_PURPLE, [
            ("IKE Parser:", "IKEv1/v2 proposals & DH groups"),
            ("ESP Tracker:", "SPI integrity & sequence jitter"),
            ("Vendor Fingerprint:", "Extracts Vendor IDs ➔ CVEs"),
            ("Data Model:", "⚡ Normalized JSON with provenance")
        ]),
        ("STAGE 3: AI INFER", INK_AMBER, [
            ("H1 / H2 Classifiers:", "Protocol & operating mode"),
            ("H3 Crypto Profile:", "Direct extraction / ESP profile"),
            ("H4 Flow Behavior:", "FFT timing (VoIP ~20ms, Video)"),
            ("H5 Outlier Isolation:", "⚡ Isolation Forest on SPI churn")
        ]),
        ("STAGE 4: ASSESS & FIX", INK_GREEN, [
            ("Rule Engine:", "NIST SP 800-77 & RFC 8247 rules"),
            ("Decoupled Scores:", "Posture (0-100) vs Risk (0-100)"),
            ("Remediation:", "1-Click Cisco, Fortinet, swanctl"),
            ("Deliverables:", "⚡ PDF, SARIF & SHA-256 Hash")
        ])
    ]

    card_w = 3.35
    card_h = 3.25
    start_x = 0.6
    gap = 0.40
    y_top = 3.75

    for idx, (title, color, items) in enumerate(stages):
        cx = start_x + idx * (card_w + gap)
        
        # Outer Card with crisp border
        card = patches.FancyBboxPatch((cx, y_top), card_w, card_h,
                                     boxstyle="round,pad=0.10,rounding_size=0.18",
                                     facecolor=CARD_BG, edgecolor=color, linewidth=2.0)
        ax.add_patch(card)
        
        # Header Badge
        t_box = patches.FancyBboxPatch((cx + 0.15, y_top + card_h - 0.54), card_w - 0.3, 0.42,
                                      boxstyle="round,pad=0.06,rounding_size=0.1",
                                      facecolor=color, edgecolor='none')
        ax.add_patch(t_box)
        ax.text(cx + card_w/2, y_top + card_h - 0.33, title,
                ha='center', va='center', fontsize=11.5, fontweight='bold', color="#FFFFFF")

        # Bullets
        by = y_top + card_h - 0.88
        for heading, text_val in items:
            is_hl = text_val.startswith("⚡")
            ax.text(cx + 0.20, by, f"• {heading}", ha='left', va='center', fontsize=9.5, fontweight='bold', color=color)
            by -= 0.28
            
            val_col = INK_GREEN if is_hl else INK_DARK
            ax.text(cx + 0.32, by, text_val, ha='left', va='center', fontsize=9.0, color=val_col, fontweight='bold' if is_hl else 'normal')
            by -= 0.34

        # Flow Arrow
        if idx < 3:
            arrow_x = cx + card_w + 0.05
            arrow_y = y_top + card_h / 2
            ax.annotate("", xy=(arrow_x + gap - 0.10, arrow_y),
                        xytext=(arrow_x, arrow_y),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.45,head_length=0.45",
                                        color=INK_BLUE, lw=2.5))

    # Bottom Left: Tech Stack Box
    stack_box = patches.FancyBboxPatch((0.6, 0.25), 7.1, 3.25,
                                      boxstyle="round,pad=0.10,rounding_size=0.18",
                                      facecolor=CARD_LIGHT, edgecolor=INK_BLUE, linewidth=2.0)
    ax.add_patch(stack_box)
    
    ax.text(4.15, 3.15, "TECHNOLOGIES & ARCHITECTURAL STACK",
            ha='center', va='center', fontsize=12.0, fontweight='bold', color=INK_BLUE)

    tech_items = [
        ("• Packet Dissection:", "Python 3.11, Scapy, tshark/dpkt, eBPF stream splitters"),
        ("• AI / Machine Learning:", "scikit-learn, XGBoost, Isolation Forest, SHAP explainability"),
        ("• Automated Testbed Lab:", "Docker-Compose, strongSwan 5.9+, iperf3, SIPp (VoIP emulator)"),
        ("• Backend & Fix Engine:", "FastAPI, SQLite, AST Multi-Vendor Configuration Fix Engine"),
        ("• Frontend Ecosystem:", "React 18 Web Dashboard + Expo Mobile SecOps Companion App")
    ]
    
    ty = 2.70
    for k, v in tech_items:
        ax.text(0.85, ty, k, ha='left', va='center', fontsize=9.5, fontweight='bold', color=INK_DARK)
        ax.text(0.85 + 2.5, ty, v, ha='left', va='center', fontsize=9.0, color=INK_BLUE)
        ty -= 0.50

    # Bottom Right: 3-Tier Evidence Taxonomy Box
    ev_box = patches.FancyBboxPatch((8.3, 0.25), 7.1, 3.25,
                                   boxstyle="round,pad=0.10,rounding_size=0.18",
                                   facecolor=CARD_LIGHT, edgecolor=INK_GREEN, linewidth=2.0)
    ax.add_patch(ev_box)

    ax.text(11.85, 3.15, "STRICT 3-TIER EVIDENCE PROVENANCE MODEL",
            ha='center', va='center', fontsize=12.0, fontweight='bold', color=INK_GREEN)

    ev_items = [
        ("✓ DIRECT (High Conf):", "IKE version, suites, DH groups, Vendor ID from cleartext wire.", INK_GREEN),
        ("~ INFERRED (Calibrated):", "Flow behavior (VoIP/Web) via timing/sizes with zero decryption.", INK_AMBER),
        ("? UNKNOWN (Never Guess):", "Post-INIT encrypted keys strictly marked Unknown to prevent errors.", INK_RED)
    ]

    ey = 2.65
    for tag, desc, col in ev_items:
        ax.text(8.55, ey, tag, ha='left', va='center', fontsize=9.5, fontweight='bold', color=col)
        ey -= 0.32
        ax.text(8.75, ey, desc, ha='left', va='center', fontsize=9.0, color=INK_DARK)
        ey -= 0.44

    ax.text(11.85, 0.55, "⚡ Core Rule: Direct facts prove crypto; ML never invents findings!",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=INK_BLUE, fontstyle='italic')

    out_png = os.path.join(out_dir, "handmade_technical_approach_slide.png")
    plt.tight_layout()
    plt.savefig(out_png, facecolor=fig.get_facecolor(), edgecolor='none', dpi=250)
    plt.savefig(os.path.join(art_dir, "handmade_technical_approach_slide.png"), facecolor=fig.get_facecolor(), edgecolor='none', dpi=250)
    plt.close()
    print("Crisp handmade slide generated successfully at:", out_png)

    # Embed directly into PPTX as Slide 3
    try:
        prs = pptx.Presentation(pptx_path)
        s3 = prs.slides[2]
        
        # Clear existing picture or card shapes on Slide 3 except Title, Footer, Number, Oval, and Logos
        for shape in list(s3.shapes):
            if shape.name.startswith("Picture") and shape.left > Inches(0.2) and shape.top > Inches(1.0):
                sp = shape._element
                sp.getparent().remove(sp)
            elif shape.name.startswith("Rounded Rectangle") or shape.name == "TextBox 8":
                sp = shape._element
                sp.getparent().remove(sp)

        # Add the graphic directly into Slide 3 content area
        s3.shapes.add_picture(out_png, Inches(0.40), Inches(1.30), Inches(12.53), Inches(5.60))
        prs.save(pptx_path)
        prs.save(mirror_pptx)
        print("Embedded handmade slide image directly into PowerPoint Slide 3!")

        # Re-export PDF
        import comtypes.client
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1
        deck = powerpoint.Presentations.Open(os.path.abspath(pptx_path))
        deck.SaveAs(os.path.abspath(pdf_path), 32)
        deck.SaveAs(os.path.abspath(mirror_pdf), 32)
        deck.Close()
        powerpoint.Quit()
        print("Updated PDF with handmade slide exported successfully!")
    except Exception as e:
        print("PPTX/PDF embedding notice:", e)

if __name__ == "__main__":
    create_crisp_handmade_slide()
