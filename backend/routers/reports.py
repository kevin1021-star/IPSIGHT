"""
CIPHER-SENTINEL: Reports router  (/api/reports)

Endpoints
---------
GET  /api/reports/{id}/pdf    – stream a PDF report
GET  /api/reports/{id}/json   – return full assessment as JSON
POST /api/reports/{id}/anchor – SHA-256 hash the report and store it (blockchain MVP)
"""

from __future__ import annotations

import hashlib
import io
import json
import logging
import uuid
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models import Assessment, AssessmentResponse, ReportHash
from ..routers.auth import get_current_user
from ..services import report_gen

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["Reports"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _get_assessment_or_404(
    assessment_id: uuid.UUID, user_id: str, db: AsyncSession
) -> Assessment:
    stmt = (
        select(Assessment)
        .where(
            Assessment.id == assessment_id,
            Assessment.user_id == user_id,
            Assessment.is_deleted == False,  # noqa: E712
        )
        .options(
            selectinload(Assessment.findings),
            selectinload(Assessment.pq_result),
            selectinload(Assessment.esp_result),
            selectinload(Assessment.report_hash),
        )
    )
    result = await db.execute(stmt)
    a = result.scalar_one_or_none()
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    return a


def _assessment_to_dict(a: Assessment) -> Dict[str, Any]:
    """Convert ORM assessment to a plain dict for JSON / hashing."""
    return AssessmentResponse.model_validate(a).model_dump(mode="json")


# ---------------------------------------------------------------------------
# GET /{id}/pdf
# ---------------------------------------------------------------------------

@router.get("/{assessment_id}/pdf", summary="Download PDF report")
async def download_pdf(
    assessment_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> StreamingResponse:
    user_id = current_user["sub"]
    a = await _get_assessment_or_404(assessment_id, user_id, db)
    data = _assessment_to_dict(a)

    pdf_bytes: bytes = report_gen.generate_pdf_report(data)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="cipher-sentinel-{assessment_id}.pdf"'
        },
    )


# ---------------------------------------------------------------------------
# GET /{id}/json
# ---------------------------------------------------------------------------

@router.get("/{assessment_id}/json", summary="Download JSON report")
async def download_json(
    assessment_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Response:
    user_id = current_user["sub"]
    a = await _get_assessment_or_404(assessment_id, user_id, db)
    data = _assessment_to_dict(a)
    json_bytes = json.dumps(data, indent=2, default=str).encode()

    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={
            "Content-Disposition": f'attachment; filename="cipher-sentinel-{assessment_id}.json"'
        },
    )


# ---------------------------------------------------------------------------
# POST /{id}/anchor
# ---------------------------------------------------------------------------

@router.post("/{assessment_id}/anchor", summary="Anchor report hash (tamper-evident audit trail)")
async def anchor_report(
    assessment_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    SHA-256 the full JSON report and store the digest in the database.
    This provides a tamper-evident audit trail; future versions will anchor
    this hash to a Hyperledger Fabric ledger.
    """
    user_id = current_user["sub"]
    a = await _get_assessment_or_404(assessment_id, user_id, db)

    if a.report_hash:
        # Already anchored — return existing record
        return {
            "assessment_id": str(assessment_id),
            "sha256_hash": a.report_hash.sha256_hash,
            "anchored_at": a.report_hash.anchored_at.isoformat(),
            "status": "already_anchored",
        }

    # Compute hash over the canonical JSON report
    data = _assessment_to_dict(a)
    canonical = json.dumps(data, sort_keys=True, default=str).encode()
    digest = hashlib.sha256(canonical).hexdigest()

    rh = ReportHash(assessment_id=assessment_id, sha256_hash=digest)
    db.add(rh)
    await db.flush()

    return {
        "assessment_id": str(assessment_id),
        "sha256_hash": digest,
        "anchored_at": rh.anchored_at.isoformat() if rh.anchored_at else None,
        "status": "anchored",
        "note": (
            "Hash stored in Neon DB. "
            "Hyperledger Fabric ledger anchoring available in v2."
        ),
    }
