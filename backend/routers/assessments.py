"""
CIPHER-SENTINEL: Assessments router  (/api/assessments)

Endpoints
---------
POST   /api/assessments/upload-pcap    – upload PCAP file → run full analysis
POST   /api/assessments/upload-config  – upload vendor config → static analysis
GET    /api/assessments/               – list user's assessments (paginated)
GET    /api/assessments/{id}           – single assessment + all related data
DELETE /api/assessments/{id}           – soft-delete an assessment
POST   /api/assessments/{id}/remediate – generate multi-vendor remediation configs

All endpoints require a valid Bearer JWT (via get_current_user dependency).
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import (
    Assessment,
    AssessmentResponse,
    AssessmentStatus,
    ESPResult,
    Finding,
    PQResult,
)
from ..routers.auth import get_current_user
from ..services import analyzer as _analyzer
from ..supabase_client import upload_file as _upload_file
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/assessments", tags=["Assessments"])


# ---------------------------------------------------------------------------
# Settings (bucket name)
# ---------------------------------------------------------------------------

class _Cfg(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    SUPABASE_BUCKET: str = "cipher-sentinel-uploads"

_cfg = _Cfg()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _assessment_to_response(a: Assessment) -> AssessmentResponse:
    """Convert ORM model to Pydantic response schema."""
    return AssessmentResponse.model_validate(a)


async def _get_assessment_or_404(
    assessment_id: uuid.UUID,
    user_id: str,
    db: AsyncSession,
) -> Assessment:
    """Fetch an assessment belonging to *user_id*, raise 404 if missing."""
    stmt = (
        select(Assessment)
        .where(
            Assessment.id == assessment_id,
            Assessment.user_id == user_id,
            Assessment.is_deleted == False,   # noqa: E712
        )
        .options(
            selectinload(Assessment.findings),
            selectinload(Assessment.pq_result),
            selectinload(Assessment.esp_result),
            selectinload(Assessment.report_hash),
        )
    )
    result = await db.execute(stmt)
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found.")
    return assessment


def _build_assessment_name(filename: str, prefix: str = "PCAP") -> str:
    """Create a human-readable assessment name from a filename."""
    stem = filename.rsplit(".", 1)[0] if "." in filename else filename
    ts   = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return f"{prefix}:{stem}:{ts}"


# ---------------------------------------------------------------------------
# POST /upload-pcap
# ---------------------------------------------------------------------------

@router.post(
    "/upload-pcap",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a PCAP file and run full IPsec analysis",
)
async def upload_pcap(
    file: UploadFile = File(..., description="PCAP capture file"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AssessmentResponse:
    user_id = current_user["sub"]
    filename = file.filename or "upload.pcap"
    pcap_bytes = await file.read()

    if not pcap_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    # Upload raw file to Supabase storage (non-blocking; ignore storage errors)
    storage_path = f"{user_id}/{uuid.uuid4().hex}/{filename}"
    public_url: Optional[str] = None
    try:
        public_url = _upload_file(_cfg.SUPABASE_BUCKET, storage_path, pcap_bytes, "application/octet-stream")
    except Exception as exc:
        logger.warning("Supabase storage upload failed (continuing analysis): %s", exc)

    # Create initial DB record in PROCESSING state
    assessment = Assessment(
        user_id=user_id,
        name=_build_assessment_name(filename, "PCAP"),
        status=AssessmentStatus.processing,
        pcap_filename=public_url or filename,
    )
    db.add(assessment)
    await db.flush()   # get the UUID assigned

    try:
        # Run heavy analysis in threadpool so event loop stays free
        result: Dict[str, Any] = await asyncio.get_event_loop().run_in_executor(
            None, _analyzer.analyze_pcap_bytes, pcap_bytes, filename
        )

        posture      = result.get("posture", {})
        pq_risk      = result.get("pq_risk", {})
        esp_results  = result.get("esp_results") or {}
        findings_lst = result.get("findings", [])
        exchange_name = result.get("exchange_name", "Unknown")
        proposals    = result.get("proposals", [])

        # Derive IKE version from exchange name
        ike_version = "IKEv2" if "IKEv2" in exchange_name or "2" in exchange_name else "IKEv1"

        # Update assessment record
        assessment.status             = AssessmentStatus.complete
        assessment.risk_score         = posture.get("posture_score", 0)
        assessment.risk_classification = posture.get("classification", "UNKNOWN")
        assessment.exchange_type      = exchange_name
        assessment.ike_version        = ike_version
        assessment.critical_violations = posture.get("critical_violations", 0)
        assessment.high_violations    = posture.get("high_violations", 0)
        assessment.medium_violations  = posture.get("medium_violations", 0)

        # Persist findings
        for f in findings_lst:
            db.add(Finding(
                assessment_id=assessment.id,
                rule_id=f.get("rule_id", ""),
                severity=f.get("severity", "LOW"),
                standard=f.get("standard", ""),
                violation=f.get("violation", ""),
                impact=f.get("impact", ""),
                remediation_goal=f.get("remediation_goal", ""),
            ))

        # Persist PQ result
        if pq_risk:
            shor = pq_risk.get("shor_algorithm_exposure", {})
            grover = pq_risk.get("grover_algorithm_exposure", {})
            db.add(PQResult(
                assessment_id=assessment.id,
                qtei_score=pq_risk.get("qtei_score", 0.0),
                threat_classification=pq_risk.get("threat_classification", "UNKNOWN"),
                hndl_risk_window=shor.get("hndl_risk_window", "Unknown"),
                shor_vulnerable=shor.get("vulnerable", False),
                grover_assessment=grover.get("assessment", ""),
                defense_action=pq_risk.get("defense_action", ""),
            ))

        # Persist ESP result
        if esp_results and "cryptographic_fingerprint" in esp_results:
            cf = esp_results["cryptographic_fingerprint"]
            om = esp_results["operational_mode_inference"]
            fs = esp_results["flow_statistics"]
            db.add(ESPResult(
                assessment_id=assessment.id,
                inferred_cipher=cf.get("inferred_cipher_category", "Unknown"),
                confidence_score=cf.get("confidence_score", 0.0),
                entropy=fs.get("avg_entropy", 0.0),
                icv_bits=cf.get("estimated_icv_bits", 0),
                operational_mode=om.get("mode", "Unknown"),
            ))

    except Exception as exc:
        logger.exception("Analysis pipeline failed for %s", filename)
        assessment.status = AssessmentStatus.failed
        await db.flush()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {exc}",
        )

    await db.flush()

    # Reload with relationships for response
    assessment_full = await _get_assessment_or_404(assessment.id, user_id, db)
    return _assessment_to_response(assessment_full)


# ---------------------------------------------------------------------------
# POST /upload-config
# ---------------------------------------------------------------------------

@router.post(
    "/upload-config",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a VPN config file for static keyword analysis",
)
async def upload_config(
    file: UploadFile = File(..., description="VPN configuration file"),
    vendor: str = Form(..., description="Vendor name: cisco | strongswan | fortinet | palo_alto | other"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AssessmentResponse:
    user_id = current_user["sub"]
    filename = file.filename or "config.txt"
    raw_bytes = await file.read()

    if not raw_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    content = raw_bytes.decode("utf-8", errors="replace")

    # Upload to Supabase storage
    storage_path = f"{user_id}/{uuid.uuid4().hex}/{filename}"
    public_url: Optional[str] = None
    try:
        public_url = _upload_file(_cfg.SUPABASE_BUCKET, storage_path, raw_bytes, "text/plain")
    except Exception as exc:
        logger.warning("Supabase storage upload failed (continuing): %s", exc)

    # Run static analysis in threadpool
    result: Dict[str, Any] = await asyncio.get_event_loop().run_in_executor(
        None, _analyzer.parse_config_file, content, vendor
    )

    posture      = result.get("posture", {})
    findings_lst = result.get("findings", [])

    assessment = Assessment(
        user_id=user_id,
        name=_build_assessment_name(filename, f"CFG:{vendor.upper()}"),
        status=AssessmentStatus.complete,
        config_filename=public_url or filename,
        vendor=vendor,
        risk_score=posture.get("posture_score", 0),
        risk_classification=posture.get("classification", "UNKNOWN"),
        critical_violations=posture.get("critical_violations", 0),
        high_violations=posture.get("high_violations", 0),
        medium_violations=posture.get("medium_violations", 0),
    )
    db.add(assessment)
    await db.flush()

    for f in findings_lst:
        db.add(Finding(
            assessment_id=assessment.id,
            rule_id=f.get("rule_id", ""),
            severity=f.get("severity", "LOW"),
            standard=f.get("standard", ""),
            violation=f.get("violation", ""),
            impact=f.get("impact", ""),
            remediation_goal=f.get("remediation_goal", ""),
        ))

    await db.flush()

    assessment_full = await _get_assessment_or_404(assessment.id, user_id, db)
    return _assessment_to_response(assessment_full)


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

@router.get(
    "/",
    response_model=List[AssessmentResponse],
    summary="List all assessments for the current user",
)
async def list_assessments(
    skip: int = Query(0, ge=0, description="Offset (pagination)"),
    limit: int = Query(20, ge=1, le=100, description="Page size"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[AssessmentResponse]:
    user_id = current_user["sub"]
    stmt = (
        select(Assessment)
        .where(Assessment.user_id == user_id, Assessment.is_deleted == False)   # noqa: E712
        .order_by(Assessment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .options(
            selectinload(Assessment.findings),
            selectinload(Assessment.pq_result),
            selectinload(Assessment.esp_result),
            selectinload(Assessment.report_hash),
        )
    )
    result = await db.execute(stmt)
    assessments = result.scalars().all()
    return [_assessment_to_response(a) for a in assessments]


# ---------------------------------------------------------------------------
# GET /{id}
# ---------------------------------------------------------------------------

@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="Get a single assessment with all findings and sub-results",
)
async def get_assessment(
    assessment_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> AssessmentResponse:
    user_id = current_user["sub"]
    assessment = await _get_assessment_or_404(assessment_id, user_id, db)
    return _assessment_to_response(assessment)


# ---------------------------------------------------------------------------
# DELETE /{id}
# ---------------------------------------------------------------------------

@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete an assessment",
)
async def delete_assessment(
    assessment_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    user_id = current_user["sub"]
    assessment = await _get_assessment_or_404(assessment_id, user_id, db)
    assessment.is_deleted = True
    await db.flush()


# ---------------------------------------------------------------------------
# POST /{id}/remediate
# ---------------------------------------------------------------------------

@router.post(
    "/{assessment_id}/remediate",
    summary="Generate multi-vendor hardened remediation configurations",
)
async def remediate(
    assessment_id: uuid.UUID,
    tunnel_name: str = Form("NTRO-SECURE-GW"),
    local_ip:    str = Form("192.168.1.1"),
    remote_ip:   str = Form("192.168.1.2"),
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    user_id = current_user["sub"]
    # Verify the assessment belongs to this user
    await _get_assessment_or_404(assessment_id, user_id, db)

    patches: Dict[str, Any] = await asyncio.get_event_loop().run_in_executor(
        None, _analyzer.generate_remediation, tunnel_name, local_ip, remote_ip
    )

    if "error" in patches:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=patches["error"],
        )

    return {
        "assessment_id": str(assessment_id),
        "tunnel_name":   tunnel_name,
        "local_ip":      local_ip,
        "remote_ip":     remote_ip,
        "configs":       patches,
    }
