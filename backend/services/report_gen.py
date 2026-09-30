"""
CIPHER-SENTINEL: PDF Report Generator (ReportLab)

Public API
----------
generate_pdf_report(assessment_data: dict) -> bytes
    Accepts the full assessment dict (matching AssessmentResponse + nested data)
    and returns raw PDF bytes ready to be streamed to the client.
"""

from __future__ import annotations

import io
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------
_NAVY    = colors.HexColor("#0A1628")
_CYAN    = colors.HexColor("#00D4FF")
_GREEN   = colors.HexColor("#00FF88")
_RED     = colors.HexColor("#FF4757")
_ORANGE  = colors.HexColor("#FFA502")
_YELLOW  = colors.HexColor("#FFD700")
_SILVER  = colors.HexColor("#8A9BB0")
_WHITE   = colors.white
_LIGHT_BG = colors.HexColor("#0D1F3C")

_SEV_COLOURS: Dict[str, Any] = {
    "CRITICAL": _RED,
    "HIGH":     _ORANGE,
    "MEDIUM":   _YELLOW,
    "LOW":      _GREEN,
    "COMPLIANT": _GREEN,
}

_SCORE_COLOUR = {
    "DEFENSE_GRADE": _GREEN,
    "ACCEPTABLE":    _YELLOW,
    "VULNERABLE":    _ORANGE,
    "COMPROMISED":   _RED,
}


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def _build_styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    styles: Dict[str, ParagraphStyle] = {}

    styles["title"] = ParagraphStyle(
        "title",
        fontSize=28,
        textColor=_CYAN,
        fontName="Helvetica-Bold",
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle",
        fontSize=13,
        textColor=_SILVER,
        fontName="Helvetica",
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    styles["section_header"] = ParagraphStyle(
        "section_header",
        fontSize=14,
        textColor=_CYAN,
        fontName="Helvetica-Bold",
        spaceBefore=14,
        spaceAfter=6,
        borderPad=4,
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontSize=9,
        textColor=colors.black,
        fontName="Helvetica",
        leading=13,
        spaceAfter=4,
    )
    styles["body_white"] = ParagraphStyle(
        "body_white",
        fontSize=9,
        textColor=_WHITE,
        fontName="Helvetica",
        leading=13,
        spaceAfter=4,
    )
    styles["kv_key"] = ParagraphStyle(
        "kv_key",
        fontSize=9,
        textColor=_SILVER,
        fontName="Helvetica-Bold",
    )
    styles["kv_val"] = ParagraphStyle(
        "kv_val",
        fontSize=9,
        textColor=colors.black,
        fontName="Helvetica",
    )
    styles["small"] = ParagraphStyle(
        "small",
        fontSize=8,
        textColor=_SILVER,
        fontName="Helvetica",
        alignment=TA_CENTER,
    )
    return styles


# ---------------------------------------------------------------------------
# Helper to draw the risk-score gauge
# ---------------------------------------------------------------------------

def _risk_gauge_table(score: int, classification: str) -> Table:
    """Returns a small table that visually represents the risk score bar."""
    filled = int(score / 10)          # 0-10 blocks
    empty  = 10 - filled

    bar_colour = _SCORE_COLOUR.get(classification, _ORANGE)

    blocks = [bar_colour] * filled + [_SILVER] * empty
    cell_data = [[""] * 10]
    tbl = Table(cell_data, colWidths=[1.4 * cm] * 10, rowHeights=[0.55 * cm])
    style_cmds = [
        ("GRID",        (0, 0), (-1, -1), 0.5, _WHITE),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [_NAVY]),
    ]
    for i, blk_colour in enumerate(blocks):
        style_cmds.append(("BACKGROUND", (i, 0), (i, 0), blk_colour))

    tbl.setStyle(TableStyle(style_cmds))
    return tbl


# ---------------------------------------------------------------------------
# Cover page elements
# ---------------------------------------------------------------------------

def _build_cover(
    story: list,
    styles: dict,
    assessment_name: str,
    risk_score: int,
    classification: str,
    created_at: str,
) -> None:
    story.append(Spacer(1, 3.5 * cm))
    story.append(Paragraph("⬡ CIPHER-SENTINEL", styles["title"]))
    story.append(Paragraph("AI-Powered IPsec VPN Security Analysis Platform", styles["subtitle"]))
    story.append(Paragraph("National Technical Research Organisation (NTRO) | SIH26160", styles["subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1, color=_CYAN, spaceAfter=16))

    story.append(Spacer(1, 1 * cm))
    story.append(Paragraph(f"Assessment Report", styles["section_header"]))
    story.append(Paragraph(f"<b>{assessment_name}</b>", ParagraphStyle(
        "aname", fontSize=16, textColor=_WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER
    )))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph(f"Generated: {created_at}", styles["small"]))
    story.append(Spacer(1, 1.5 * cm))

    # Risk score block
    score_colour = _SCORE_COLOUR.get(classification, _ORANGE)
    score_data = [
        [
            Paragraph("SECURITY POSTURE SCORE", ParagraphStyle(
                "sp_label", fontSize=9, textColor=_SILVER, fontName="Helvetica-Bold",
                alignment=TA_CENTER
            )),
        ],
        [
            Paragraph(
                f'<font size="48" color="{score_colour.hexval()}">'
                f'<b>{risk_score}</b></font><font size="20" color="{_SILVER.hexval()}"> / 100</font>',
                ParagraphStyle("score_val", alignment=TA_CENTER)
            ),
        ],
        [
            Paragraph(
                f'<font color="{score_colour.hexval()}"><b>{classification}</b></font>',
                ParagraphStyle("class_val", fontSize=14, alignment=TA_CENTER)
            ),
        ],
    ]
    score_tbl = Table(score_data, colWidths=[10 * cm])
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), _NAVY),
        ("BOX",         (0, 0), (-1, -1), 1.5, _CYAN),
        ("TOPPADDING",  (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
        ("ALIGN",       (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(score_tbl)
    story.append(Spacer(1, 0.5 * cm))
    story.append(_risk_gauge_table(risk_score, classification))
    story.append(PageBreak())


# ---------------------------------------------------------------------------
# Executive summary
# ---------------------------------------------------------------------------

def _build_executive_summary(
    story: list,
    styles: dict,
    data: Dict[str, Any],
) -> None:
    story.append(Paragraph("1. Executive Summary", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_CYAN, spaceAfter=8))

    crit = data.get("critical_violations", 0)
    high = data.get("high_violations", 0)
    med  = data.get("medium_violations", 0)

    summary_rows = [
        ["Metric", "Value"],
        ["Assessment Name",    data.get("name", "N/A")],
        ["Analysis Status",    data.get("status", "N/A").upper()],
        ["Posture Score",      f"{data.get('risk_score', 0)} / 100"],
        ["Classification",     data.get("risk_classification", "N/A")],
        ["Exchange Type",      data.get("exchange_type", "N/A") or "N/A"],
        ["IKE Version",        data.get("ike_version", "N/A") or "N/A"],
        ["Vendor / Platform",  data.get("vendor", "N/A") or "N/A"],
        ["Critical Violations",str(crit)],
        ["High Violations",    str(high)],
        ["Medium Violations",  str(med)],
        ["Total Findings",     str(crit + high + med)],
    ]
    tbl = Table(summary_rows, colWidths=[7 * cm, 10 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  _NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  _CYAN),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#F5F7FA"), _WHITE]),
        ("GRID",         (0, 0), (-1, -1), 0.4, _SILVER),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5 * cm))


# ---------------------------------------------------------------------------
# Findings table
# ---------------------------------------------------------------------------

def _build_findings(story: list, styles: dict, findings: List[Dict[str, Any]]) -> None:
    story.append(Paragraph("2. Formal Cryptographic Invariant Violations", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_CYAN, spaceAfter=8))

    if not findings:
        story.append(Paragraph("✓ No violations detected. Proposal is cryptographically compliant.", styles["body"]))
        story.append(Spacer(1, 0.3 * cm))
        return

    header = ["Rule ID", "Severity", "Standard", "Violation", "Impact", "Remediation Goal"]
    col_widths = [2.2 * cm, 1.8 * cm, 3.5 * cm, 4.2 * cm, 3.8 * cm, 3.5 * cm]

    rows = [header]
    style_cmds: list = [
        ("BACKGROUND",   (0, 0), (-1, 0), _NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0), _CYAN),
        ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 7.5),
        ("GRID",         (0, 0), (-1, -1), 0.3, _SILVER),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
        ("LEFTPADDING",  (0, 0), (-1, -1), 4),
        ("WORDWRAP",     (0, 0), (-1, -1), True),
    ]

    for i, f in enumerate(findings, start=1):
        sev = f.get("severity", "LOW")
        sev_colour = _SEV_COLOURS.get(sev, _SILVER)
        row = [
            f.get("rule_id", ""),
            Paragraph(f'<font color="{sev_colour.hexval()}"><b>{sev}</b></font>',
                      ParagraphStyle("sev_cell", fontSize=7.5)),
            f.get("standard", ""),
            f.get("violation", ""),
            f.get("impact", ""),
            f.get("remediation_goal", ""),
        ]
        rows.append(row)
        bg = colors.HexColor("#F5F7FA") if i % 2 == 0 else _WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))

    tbl = Table(rows, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle(style_cmds))
    story.append(KeepTogether([tbl]))
    story.append(Spacer(1, 0.5 * cm))


# ---------------------------------------------------------------------------
# Post-Quantum section
# ---------------------------------------------------------------------------

def _build_pq_section(story: list, styles: dict, pq: Dict[str, Any]) -> None:
    story.append(Paragraph("3. Post-Quantum Threat Assessment (HNDL)", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_CYAN, spaceAfter=8))

    qtei   = pq.get("qtei_score", 0.0)
    t_class = pq.get("threat_classification", "UNKNOWN")
    shor   = pq.get("shor_algorithm_exposure", {})
    grover = pq.get("grover_algorithm_exposure", {})
    defense = pq.get("defense_action", "N/A")

    colour = _RED if qtei > 0.7 else _ORANGE if qtei > 0.3 else _GREEN

    pq_rows = [
        ["Parameter", "Value"],
        ["Quantum Threat Exposure Index (QTEI)", f"{qtei:.3f}  (0 = safe, 1 = critical)"],
        ["Threat Classification", t_class],
        ["Shor Vulnerable",       str(shor.get("vulnerable", False))],
        ["HNDL Risk Window",      shor.get("hndl_risk_window", "N/A")],
        ["Est. Qubits to Break",  shor.get("estimated_logical_qubits_needed", "N/A")],
        ["Grover Assessment",     grover.get("assessment", "N/A")],
        ["Effective Quantum Bits",str(grover.get("effective_quantum_bits", "N/A"))],
        ["Recommended Action",    defense],
    ]
    tbl = Table(pq_rows, colWidths=[7 * cm, 12 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  _NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  _CYAN),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#F5F7FA"), _WHITE]),
        ("GRID",         (0, 0), (-1, -1), 0.4, _SILVER),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",    (0, 2), (1, 2),   colour),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5 * cm))


# ---------------------------------------------------------------------------
# ESP section
# ---------------------------------------------------------------------------

def _build_esp_section(story: list, styles: dict, esp: Dict[str, Any]) -> None:
    story.append(Paragraph("4. Passive ESP Side-Channel Inference (Patent Claim 1)", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_CYAN, spaceAfter=8))

    cf  = esp.get("cryptographic_fingerprint", {})
    om  = esp.get("operational_mode_inference", {})
    fs  = esp.get("flow_statistics", {})

    esp_rows = [
        ["Inference Dimension", "Derived Specification", "Confidence"],
        ["VPN Operating Mode",       om.get("mode", "N/A"),  f"{om.get('confidence_percentage', 0)}%"],
        ["Cipher Family",            cf.get("inferred_cipher_category", "N/A"), f"{int(cf.get('confidence_score', 0) * 100)}%"],
        ["Block Size",               f"{cf.get('inferred_block_size_bytes', 0)} bytes", "—"],
        ["Ciphertext Shannon Entropy",f"{fs.get('avg_entropy', 0):.4f} bits/byte", "100%"],
        ["ICV Auth Tag",             f"~{cf.get('estimated_icv_bits', 0)} bits", "92%"],
        ["Entropy Status",           cf.get("entropy_status", "N/A"), "—"],
        ["Packet Count",             str(fs.get("packet_count", 0)), "—"],
        ["Sequence Continuity",      fs.get("sequence_continuity", "N/A"), "—"],
    ]
    tbl = Table(esp_rows, colWidths=[6 * cm, 8 * cm, 5 * cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  _NAVY),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  _CYAN),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#F5F7FA"), _WHITE]),
        ("GRID",         (0, 0), (-1, -1), 0.4, _SILVER),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5 * cm))


# ---------------------------------------------------------------------------
# Remediation section
# ---------------------------------------------------------------------------

def _build_remediation_section(story: list, styles: dict, remediation: Dict[str, str]) -> None:
    story.append(Paragraph("5. Autonomous Remediation Configurations", styles["section_header"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=_CYAN, spaceAfter=8))

    vendor_labels = {
        "strongswan_swanctl": "StrongSwan swanctl.conf",
        "cisco_iosxe":        "Cisco IOS-XE",
        "fortinet_fortios":   "Fortinet FortiOS",
        "ansible_playbook":   "Ansible Playbook (YAML)",
    }

    code_style = ParagraphStyle(
        "code",
        fontSize=7,
        fontName="Courier",
        textColor=_GREEN,
        backColor=_NAVY,
        leftIndent=6,
        rightIndent=6,
        spaceAfter=8,
        leading=10,
    )

    for key, label in vendor_labels.items():
        code = remediation.get(key, "")
        if not code:
            continue
        story.append(Paragraph(f"<b>{label}</b>", styles["body"]))
        # Escape special chars for Paragraph
        safe_code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        lines = safe_code.split("\n")[:60]   # cap at 60 lines for PDF readability
        story.append(Paragraph("<br/>".join(lines), code_style))


# ---------------------------------------------------------------------------
# Footer / header callbacks
# ---------------------------------------------------------------------------

def _header_footer(canvas: Any, doc: Any) -> None:
    canvas.saveState()
    width, height = A4

    # Header bar
    canvas.setFillColor(_NAVY)
    canvas.rect(0, height - 28, width, 28, fill=True, stroke=False)
    canvas.setFillColor(_CYAN)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.2 * cm, height - 18, "CIPHER-SENTINEL | RESTRICTED SECURITY REPORT")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(_SILVER)
    canvas.drawRightString(width - 1.2 * cm, height - 18, datetime.utcnow().strftime("%Y-%m-%d UTC"))

    # Footer bar
    canvas.setFillColor(_NAVY)
    canvas.rect(0, 0, width, 22, fill=True, stroke=False)
    canvas.setFillColor(_SILVER)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.2 * cm, 7, "Confidential — For Authorized Personnel Only")
    canvas.drawRightString(width - 1.2 * cm, 7, f"Page {doc.page}")

    canvas.restoreState()


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_pdf_report(assessment_data: Dict[str, Any]) -> bytes:
    """
    Generate a professional CIPHER-SENTINEL PDF report.

    Parameters
    ----------
    assessment_data : dict
        Full assessment dict containing at minimum the keys produced by
        AssessmentResponse plus optional 'pq_result', 'esp_result',
        and 'remediation' sub-dicts.

    Returns
    -------
    bytes
        Raw PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=1.5 * cm,
        title=f"CIPHER-SENTINEL — {assessment_data.get('name', 'Assessment')}",
        author="CIPHER-SENTINEL AI Engine",
    )

    styles = _build_styles()
    story: list = []

    # --- Cover page ---
    created_raw = assessment_data.get("created_at", "")
    if isinstance(created_raw, datetime):
        created_str = created_raw.strftime("%Y-%m-%d %H:%M UTC")
    else:
        created_str = str(created_raw)[:19] if created_raw else datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    _build_cover(
        story,
        styles,
        assessment_name=assessment_data.get("name", "Untitled Assessment"),
        risk_score=assessment_data.get("risk_score", 0),
        classification=assessment_data.get("risk_classification", "UNKNOWN"),
        created_at=created_str,
    )

    # --- Executive summary ---
    _build_executive_summary(story, styles, assessment_data)

    # --- Findings ---
    findings = assessment_data.get("findings", [])
    if isinstance(findings, list) and findings and hasattr(findings[0], "__dict__"):
        # Pydantic objects → dicts
        findings = [f.__dict__ if hasattr(f, "__dict__") else dict(f) for f in findings]
    _build_findings(story, styles, findings)

    # --- PQ section ---
    pq = assessment_data.get("pq_result") or assessment_data.get("pq_risk") or {}
    if pq:
        if hasattr(pq, "__dict__"):
            pq = vars(pq)
        _build_pq_section(story, styles, pq)

    # --- ESP section ---
    esp = assessment_data.get("esp_result") or assessment_data.get("esp_results") or {}
    if esp:
        if hasattr(esp, "__dict__"):
            esp = vars(esp)
        # ESP result from DB is flat; ESP from analyzer has nested keys
        if "cryptographic_fingerprint" not in esp:
            # Reconstruct nested structure from flat DB model
            esp = {
                "cryptographic_fingerprint": {
                    "inferred_cipher_category": esp.get("inferred_cipher", "N/A"),
                    "inferred_block_size_bytes": 0,
                    "estimated_icv_bits": esp.get("icv_bits", 0),
                    "entropy_status": "HIGH_CONFIDENTIALITY",
                    "confidence_score": esp.get("confidence_score", 0.0),
                },
                "operational_mode_inference": {
                    "mode": esp.get("operational_mode", "N/A"),
                    "confidence_percentage": int(esp.get("confidence_score", 0) * 100),
                    "evidence": "Derived from packet payload analysis",
                },
                "flow_statistics": {
                    "packet_count": 0,
                    "avg_entropy": esp.get("entropy", 0.0),
                    "sequence_continuity": "N/A",
                },
            }
        _build_esp_section(story, styles, esp)

    # --- Remediation section ---
    remediation = assessment_data.get("remediation") or {}
    if remediation and not remediation.get("error"):
        _build_remediation_section(story, styles, remediation)

    # Build PDF
    try:
        doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    except Exception:
        logger.exception("ReportLab doc.build() failed")
        raise

    buffer.seek(0)
    return buffer.read()
