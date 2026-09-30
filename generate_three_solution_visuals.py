"""
Generate 3 High-Resolution, Defense-Grade Visual Diagrams for IPsight Slide 2 Sections:
1. Detailed Explanation of the Proposed Solution (Workflow & Pipeline)
2. How It Addresses the Problem (Problem vs Solution Infographic)
3. Innovation & Uniqueness of the Solution (4 Novelty Pillars)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Set global styles
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

out_dir = r"C:\Users\AS\Downloads\vpn"
art_dir = r"C:\Users\AS\.gemini\antigravity\brain\eb8c9836-bba9-4526-a239-b44851c8fe47"

# Color Palette
BG_DARK = "#0F172A"       # Slate 900
CARD_BG = "#1E293B"       # Slate 800
CARD_BORDER = "#334155"   # Slate 700
BLUE_ACCENT = "#0284C7"   # Sky 600
BLUE_LIGHT = "#38BDF8"    # Sky 400
GREEN_ACCENT = "#10B981"  # Emerald 500
AMBER_ACCENT = "#F59E0B"  # Amber 500
RED_ACCENT = "#EF4444"    # Red 500
PURPLE_ACCENT = "#8B5CF6" # Violet 500
TEXT_WHITE = "#F8FAFC"    # Slate 50
TEXT_MUTED = "#94A3B8"    # Slate 400

# =============================================================================
# VISUAL 1: PROPOSED SOLUTION & PIPELINE WORKFLOW
# =============================================================================
def generate_visual_1():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitle
    ax.text(8, 8.4, "IPSIGHT — AUTOMATED ZERO-TOUCH AUDIT PIPELINE", 
            ha='center', va='center', fontsize=18, fontweight='bold', color=TEXT_WHITE)
    ax.text(8, 7.9, "Seamless End-to-End Workflow from Raw Traffic to Multi-Vendor Automated Fixes", 
            ha='center', va='center', fontsize=12, color=BLUE_LIGHT, fontstyle='italic')

    # 4 Main Pipeline Stages
    stages = [
        ("STAGE 1: INGEST", BLUE_ACCENT, [
            "• PCAP & Live Network Streams",
            "• strongSwan / Router Configs",
            "• UDP 500/4500 & ESP Splitter",
            "• 5-Tuple + SPI Sessionizer",
            "⚡ 100MB PCAP in <2 minutes"
        ]),
        ("STAGE 2: DISSECT", PURPLE_ACCENT, [
            "• IKEv1 / IKEv2 State Dissection",
            "• Crypto Transform Proposals",
            "• Vendor ID Fingerprinting",
            "• Sequence Jitter & NAT-T/DPD",
            "⚡ Normalized JSON + Provenance"
        ]),
        ("STAGE 3: AI INFER", AMBER_ACCENT, [
            "• H1/H2: Protocol & Mode Classifier",
            "• H3: ESP Crypto Profile Inference",
            "• H4: Calibrated Flow AI (VoIP/Web)",
            "• H5: Isolation Forest Outliers",
            "⚡ Zero-Decryption Metadata AI"
        ]),
        ("STAGE 4: ASSESS & FIX", GREEN_ACCENT, [
            "• Deterministic YAML Rule Engine",
            "• NIST SP 800-77 / RFC 8247 Rules",
            "• Dual Posture & Risk Scoring",
            "• 1-Click Multi-Vendor Fixes",
            "⚡ Cisco, Fortinet, strongSwan"
        ])
    ]

    card_w = 3.3
    card_h = 3.4
    start_x = 0.8
    spacing = 3.8
    y_pos = 4.0

    for idx, (title, color, items) in enumerate(stages):
        cx = start_x + idx * spacing
        # Draw Card
        rect = patches.FancyBboxPatch((cx, y_pos), card_w, card_h,
                                      boxstyle="round,pad=0.15,rounding_size=0.2",
                                      facecolor=CARD_BG, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        
        # Header Badge
        header_rect = patches.FancyBboxPatch((cx + 0.15, y_pos + card_h - 0.6), card_w - 0.3, 0.45,
                                            boxstyle="round,pad=0.08,rounding_size=0.1",
                                            facecolor=color, edgecolor='none')
        ax.add_patch(header_rect)
        ax.text(cx + card_w/2, y_pos + card_h - 0.38, title, 
                ha='center', va='center', fontsize=11, fontweight='bold', color=TEXT_WHITE)

        # Bullet Points
        item_y = y_pos + card_h - 0.95
        for it in items:
            is_highlight = it.startswith("⚡")
            text_color = GREEN_ACCENT if is_highlight else TEXT_WHITE
            font_wt = 'bold' if is_highlight else 'normal'
            ax.text(cx + 0.25, item_y, it, ha='left', va='center', fontsize=9.5, color=text_color, fontweight=font_wt)
            item_y -= 0.48

        # Flow Arrows
        if idx < 3:
            arrow_x = cx + card_w + 0.08
            arrow_y = y_pos + card_h / 2
            ax.annotate("", xy=(arrow_x + 0.34, arrow_y), xytext=(arrow_x, arrow_y),
                        arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.4", color=BLUE_LIGHT, lw=3))

    # Bottom Delivery Ecosystem Section
    eco_rect = patches.FancyBboxPatch((0.8, 0.7), 14.4, 2.7,
                                     boxstyle="round,pad=0.15,rounding_size=0.2",
                                     facecolor="#131D31", edgecolor=BLUE_LIGHT, linewidth=1.5)
    ax.add_patch(eco_rect)
    ax.text(8, 3.05, "MULTI-PLATFORM OPERATIONAL ECOSYSTEM & REMEDIATION DELIVERY", 
            ha='center', va='center', fontsize=11.5, fontweight='bold', color=BLUE_LIGHT)

    eco_cols = [
        ("WEB DASHBOARD (React 18)", BLUE_ACCENT, "Real-time SA inventory, dynamic filter matrices, tunnel compliance scorecards, and interactive CVE link maps."),
        ("MOBILE SECOPS APP (Expo)", PURPLE_ACCENT, "Pocket executive scorecard, instant push alerts on downgrade attacks, and 1-tap remote CLI fix execution."),
        ("AUDIT REPORTS (PDF / SARIF)", GREEN_ACCENT, "Executive heat-maps, NIST SP 800-77 compliance matrices, and SHA-256 tamper-evident integrity hashes.")
    ]

    for c_idx, (c_title, c_color, c_desc) in enumerate(eco_cols):
        c_x = 1.2 + c_idx * 4.6
        c_rect = patches.FancyBboxPatch((c_x, 1.0), 4.2, 1.7,
                                        boxstyle="round,pad=0.1,rounding_size=0.15",
                                        facecolor=CARD_BG, edgecolor=c_color, linewidth=1.2)
        ax.add_patch(c_rect)
        ax.text(c_x + 2.1, 2.35, c_title, ha='center', va='center', fontsize=10, fontweight='bold', color=c_color)
        
        # Wrap description into lines
        words = c_desc.split()
        lines = []
        curr = ""
        for w in words:
            if len(curr + " " + w) < 42:
                curr += " " + w
            else:
                lines.append(curr.strip())
                curr = w
        if curr:
            lines.append(curr.strip())
            
        desc_y = 1.90
        for ln in lines:
            ax.text(c_x + 0.2, desc_y, ln, ha='left', va='center', fontsize=8.5, color=TEXT_WHITE)
            desc_y -= 0.32

    out_file1 = os.path.join(out_dir, "visual_1_proposed_solution.png")
    plt.tight_layout()
    plt.savefig(out_file1, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.savefig(os.path.join(art_dir, "visual_1_proposed_solution.png"), facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print("Visual 1 saved successfully.")

# =============================================================================
# VISUAL 2: HOW IT ADDRESSES THE PROBLEM (PROBLEM VS SOLUTION MATRIX)
# =============================================================================
def generate_visual_2():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitle
    ax.text(8, 8.4, "HOW IPSIGHT RESOLVES CRITICAL IPSEC AUDIT BOTTLENECKS", 
            ha='center', va='center', fontsize=18, fontweight='bold', color=TEXT_WHITE)
    ax.text(8, 7.9, "Transforming Broken Manual Auditing into Automated, Zero-Decryption Wire-Truth Visibility", 
            ha='center', va='center', fontsize=12, color=BLUE_LIGHT, fontstyle='italic')

    # 4 Problem-Solution Comparative Cards
    comparisons = [
        ("1. AUDIT LATENCY", 
         "THE BROKEN REALITY", RED_ACCENT, "Manual Wireshark packet capture analysis takes 3–5 days per gateway; requires scarce crypto engineering talent.",
         "THE IPSIGHT RESOLUTION", GREEN_ACCENT, "Sub-2 minute automated audits; parses 100MB PCAP in <2 min and config files in <5 sec with zero manual effort."),
        
        ("2. CRYPTO COMPLIANCE", 
         "THE BROKEN REALITY", RED_ACCENT, "Hidden legacy suites (3DES, SHA-1, DH <14) & silent responder downgrade attacks operate completely undetected.",
         "THE IPSIGHT RESOLUTION", GREEN_ACCENT, "Automated RFC 8247 & NIST SP 800-77r1 checks isolate weak transforms, IKEv1 Historic status & PSK leaks immediately."),

        ("3. ENCRYPTED VISIBILITY", 
         "THE BROKEN REALITY", RED_ACCENT, "ESP tunnels are opaque black boxes; admins have zero visibility into in-tunnel traffic types without decrypting.",
         "THE IPSIGHT RESOLUTION", GREEN_ACCENT, "Calibrated AI infers VoIP, Web, Video, and Bulk flows via packet sizes & FFT periodicity with ZERO payload decryption."),

        ("4. REMEDIATION EFFORT", 
         "THE BROKEN REALITY", RED_ACCENT, "Audit reports leave admins with generic text findings; manual script writing leads to syntax errors and outages.",
         "THE IPSIGHT RESOLUTION", GREEN_ACCENT, "1-Click automated AST fix engine generates copy-paste native CLI patches for Cisco IOS-XE, Fortinet & strongSwan.")
    ]

    card_w = 7.0
    card_h = 2.9
    
    positions = [
        (0.8, 4.4),   # Card 1: Top Left
        (8.2, 4.4),   # Card 2: Top Right
        (0.8, 1.1),   # Card 3: Bottom Left
        (8.2, 1.1)    # Card 4: Bottom Right
    ]

    for idx, (title, p_label, p_color, p_desc, s_label, s_color, s_desc) in enumerate(comparisons):
        x, y = positions[idx]
        
        # Outer Card
        card = patches.FancyBboxPatch((x, y), card_w, card_h,
                                     boxstyle="round,pad=0.15,rounding_size=0.2",
                                     facecolor=CARD_BG, edgecolor=CARD_BORDER, linewidth=1.5)
        ax.add_patch(card)
        
        # Card Header
        ax.text(x + 0.3, y + card_h - 0.35, title, ha='left', va='center', fontsize=12, fontweight='bold', color=BLUE_LIGHT)

        # Problem Box (Left Sub-box)
        p_box = patches.FancyBboxPatch((x + 0.25, y + 0.25), 3.1, 2.0,
                                       boxstyle="round,pad=0.08,rounding_size=0.1",
                                       facecolor="#2A171A", edgecolor=p_color, linewidth=1.2)
        ax.add_patch(p_box)
        ax.text(x + 0.45, y + 1.95, f"▲ {p_label}", ha='left', va='center', fontsize=9.0, fontweight='bold', color=p_color)
        
        # Text wrap problem
        words_p = p_desc.split()
        lines_p = []
        curr = ""
        for w in words_p:
            if len(curr + " " + w) < 28:
                curr += " " + w
            else:
                lines_p.append(curr.strip())
                curr = w
        if curr:
            lines_p.append(curr.strip())
        
        py = y + 1.55
        for lp in lines_p:
            ax.text(x + 0.45, py, lp, ha='left', va='center', fontsize=8.0, color=TEXT_WHITE)
            py -= 0.28

        # Solution Box (Right Sub-box)
        s_box = patches.FancyBboxPatch((x + 3.65, y + 0.25), 3.1, 2.0,
                                       boxstyle="round,pad=0.08,rounding_size=0.1",
                                       facecolor="#132B23", edgecolor=s_color, linewidth=1.2)
        ax.add_patch(s_box)
        ax.text(x + 3.85, y + 1.95, f"✓ {s_label}", ha='left', va='center', fontsize=9.0, fontweight='bold', color=s_color)

        # Text wrap solution
        words_s = s_desc.split()
        lines_s = []
        curr = ""
        for w in words_s:
            if len(curr + " " + w) < 28:
                curr += " " + w
            else:
                lines_s.append(curr.strip())
                curr = w
        if curr:
            lines_s.append(curr.strip())
            
        sy = y + 1.55
        for ls in lines_s:
            ax.text(x + 3.85, sy, ls, ha='left', va='center', fontsize=8.0, color=TEXT_WHITE)
            sy -= 0.28

    out_file2 = os.path.join(out_dir, "visual_2_how_it_addresses_problem.png")
    plt.tight_layout()
    plt.savefig(out_file2, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.savefig(os.path.join(art_dir, "visual_2_how_it_addresses_problem.png"), facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print("Visual 2 saved successfully.")

# =============================================================================
# VISUAL 3: INNOVATION & UNIQUENESS OF THE SOLUTION (4 NOVELTY PILLARS)
# =============================================================================
def generate_visual_3():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title & Subtitle
    ax.text(8, 8.4, "IPSIGHT — 4 DEFENSE-GRADE NOVELTY PILLARS", 
            ha='center', va='center', fontsize=18, fontweight='bold', color=TEXT_WHITE)
    ax.text(8, 7.9, "Pioneering Evidence-Aware Machine Intelligence Grounded in Cryptographic Wire Truth", 
            ha='center', va='center', fontsize=12, color=GREEN_ACCENT, fontstyle='italic')

    # 4 Novelty Pillars
    pillars = [
        ("PILLAR 1", "3-TIER EVIDENCE TAXONOMY", BLUE_ACCENT, [
            ("Direct Wire Facts:", "IKE version, transforms, DH groups & Vendor IDs read verbatim from wire."),
            ("Inferred Profiles:", "Flow behaviors with calibrated confidence; zero payload decryption."),
            ("Strict Unknowns:", "Unseen encrypted keys/PFS marked Unknown to eliminate false claims.")
        ], "⚡ Zero AI Guessing"),
        ("PILLAR 2", "CALIBRATED BEHAVIORAL AI", PURPLE_ACCENT, [
            ("FFT Timing Analysis:", "VoIP ~20ms metronomic inter-arrival periodicity detection."),
            ("Isotonic Calibration:", "Brier score minimization ensuring honest confidence metrics."),
            ("SHAP Explainability:", "Feature attribution for packet burst, symmetry, and size entropy.")
        ], "⚡ Zero-Decryption AI"),
        ("PILLAR 3", "DECOUPLED DUAL SCORING", AMBER_ACCENT, [
            ("Security Posture (0-100):", "Evaluates NIST SP 800-77 & RFC 8247 compliance strength."),
            ("Risk Urgency (0-100):", "Quantifies threat exploitability and immediate attack surface."),
            ("Threat Matrix:", "Likelihood × Impact matrix to prioritize critical SecOps fixes.")
        ], "⚡ Actionable Triage"),
        ("PILLAR 4", "POST-QUANTUM (PQC) RUNWAY", GREEN_ACCENT, [
            ("Quantum Risk Flagging:", "Flags classical DH against NSA CNSA 2.0 migration timelines."),
            ("Hybrid Migration:", "RFC 9370 & RFC 9242 ML-KEM post-quantum exchange readiness."),
            ("HNDL Mitigation:", "Defends sovereign communications from 'Harvest Now, Decrypt Later'.")
        ], "⚡ National Quantum Shield")
    ]

    card_w = 3.3
    card_h = 6.2
    start_x = 0.8
    spacing = 3.8
    y_pos = 1.0

    for idx, (pill_num, pill_title, color, items, footer_tag) in enumerate(pillars):
        cx = start_x + idx * spacing
        
        # Pillar Outer Card
        card = patches.FancyBboxPatch((cx, y_pos), card_w, card_h,
                                     boxstyle="round,pad=0.15,rounding_size=0.2",
                                     facecolor=CARD_BG, edgecolor=color, linewidth=2.0)
        ax.add_patch(card)
        
        # Pillar Header Badge
        header_rect = patches.FancyBboxPatch((cx + 0.15, y_pos + card_h - 0.85), card_w - 0.3, 0.65,
                                            boxstyle="round,pad=0.08,rounding_size=0.12",
                                            facecolor=color, edgecolor='none')
        ax.add_patch(header_rect)
        ax.text(cx + card_w/2, y_pos + card_h - 0.40, pill_num, 
                ha='center', va='center', fontsize=10.0, fontweight='bold', color=TEXT_WHITE)
        ax.text(cx + card_w/2, y_pos + card_h - 0.65, pill_title, 
                ha='center', va='center', fontsize=8.5, fontweight='bold', color=TEXT_WHITE)

        # Content Items
        item_y = y_pos + card_h - 1.25
        for heading, body in items:
            ax.text(cx + 0.25, item_y, f"• {heading}", ha='left', va='center', fontsize=9.5, color=color, fontweight='bold')
            item_y -= 0.35
            
            # Wrap body
            words = body.split()
            lines = []
            curr = ""
            for w in words:
                if len(curr + " " + w) < 28:
                    curr += " " + w
                else:
                    lines.append(curr.strip())
                    curr = w
            if curr:
                lines.append(curr.strip())
                
            for ln in lines:
                ax.text(cx + 0.35, item_y, ln, ha='left', va='center', fontsize=8.5, color=TEXT_WHITE)
                item_y -= 0.30
            item_y -= 0.20

        # Footer highlight badge
        ft_rect = patches.FancyBboxPatch((cx + 0.20, y_pos + 0.25), card_w - 0.4, 0.50,
                                        boxstyle="round,pad=0.06,rounding_size=0.1",
                                        facecolor="#132B23" if color == GREEN_ACCENT else "#1E2235", 
                                        edgecolor=color, linewidth=1.0)
        ax.add_patch(ft_rect)
        ax.text(cx + card_w/2, y_pos + 0.50, footer_tag, ha='center', va='center', fontsize=9.0, fontweight='bold', color=color)

    out_file3 = os.path.join(out_dir, "visual_3_innovation_and_uniqueness.png")
    plt.tight_layout()
    plt.savefig(out_file3, facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.savefig(os.path.join(art_dir, "visual_3_innovation_and_uniqueness.png"), facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
    plt.close()
    print("Visual 3 saved successfully.")

if __name__ == "__main__":
    generate_visual_1()
    generate_visual_2()
    generate_visual_3()
    print("All 3 visuals generated successfully!")
