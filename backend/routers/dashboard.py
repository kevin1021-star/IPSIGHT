"""
CIPHER-SENTINEL: Dashboard router  (/api/dashboard)

Endpoints
---------
GET /api/dashboard/stats   – aggregate stats for the current user
GET /api/dashboard/trends  – avg risk score per day for last 30 days
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select, case
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models import Assessment, Finding, DashboardStats
from ..routers.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats, summary="Dashboard aggregate statistics")
async def get_stats(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardStats:
    user_id = current_user["sub"]

    # Base condition
    base_cond = (
        Assessment.user_id == user_id,
        Assessment.is_deleted == False,  # noqa: E712
        Assessment.status == "complete",
    )

    # Total assessments
    total_q = await db.execute(
        select(func.count(Assessment.id)).where(*base_cond)
    )
    total: int = total_q.scalar_one() or 0

    # Average risk score
    avg_q = await db.execute(
        select(func.avg(Assessment.risk_score)).where(*base_cond)
    )
    avg_score: float = round(float(avg_q.scalar_one() or 0), 1)

    # Violation sums
    viol_q = await db.execute(
        select(
            func.sum(Assessment.critical_violations),
            func.sum(Assessment.high_violations),
        ).where(*base_cond)
    )
    row = viol_q.one()
    critical_total: int = int(row[0] or 0)
    high_total: int = int(row[1] or 0)

    # Recent 5 assessments
    recent_q = await db.execute(
        select(
            Assessment.id,
            Assessment.name,
            Assessment.risk_score,
            Assessment.risk_classification,
            Assessment.vendor,
            Assessment.created_at,
        )
        .where(*base_cond)
        .order_by(Assessment.created_at.desc())
        .limit(5)
    )
    recent = [
        {
            "id": str(r.id),
            "name": r.name,
            "risk_score": r.risk_score,
            "risk_classification": r.risk_classification,
            "vendor": r.vendor,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in recent_q.all()
    ]

    # Severity distribution (from findings)
    sev_q = await db.execute(
        select(Finding.severity, func.count(Finding.id))
        .join(Assessment, Assessment.id == Finding.assessment_id)
        .where(Assessment.user_id == user_id, Assessment.is_deleted == False)  # noqa: E712
        .group_by(Finding.severity)
    )
    severity_dist: Dict[str, int] = {row[0]: row[1] for row in sev_q.all()}

    # Vendor distribution
    vend_q = await db.execute(
        select(Assessment.vendor, func.count(Assessment.id))
        .where(*base_cond, Assessment.vendor != None)  # noqa: E711
        .group_by(Assessment.vendor)
    )
    vendor_dist: Dict[str, int] = {
        (row[0] or "Unknown"): row[1] for row in vend_q.all()
    }

    return DashboardStats(
        total_assessments=total,
        critical_count=critical_total,
        high_count=high_total,
        avg_risk_score=avg_score,
        recent_assessments=recent,
        severity_distribution=severity_dist,
        vendor_distribution=vendor_dist,
    )


@router.get("/trends", summary="Risk score trends over the last 30 days")
async def get_trends(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    user_id = current_user["sub"]
    since = datetime.now(timezone.utc) - timedelta(days=30)

    trends_q = await db.execute(
        select(
            func.date(Assessment.created_at).label("date"),
            func.avg(Assessment.risk_score).label("avg_score"),
            func.count(Assessment.id).label("count"),
        )
        .where(
            Assessment.user_id == user_id,
            Assessment.is_deleted == False,  # noqa: E712
            Assessment.status == "complete",
            Assessment.created_at >= since,
        )
        .group_by(func.date(Assessment.created_at))
        .order_by(func.date(Assessment.created_at))
    )

    return [
        {
            "date": str(row.date),
            "avg_score": round(float(row.avg_score), 1),
            "count": row.count,
        }
        for row in trends_q.all()
    ]
