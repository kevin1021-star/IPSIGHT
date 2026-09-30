"""
CIPHER-SENTINEL: SQLAlchemy ORM models + Pydantic response schemas.

ORM tables
----------
Assessment  – one per analysis run
Finding     – N formal-verification violations per assessment
PQResult    – one post-quantum risk record per assessment
ESPResult   – one ESP side-channel record per assessment
ReportHash  – SHA-256 anchoring record for integrity / audit trail

Pydantic schemas (suffix *Response) are used by FastAPI response_model fields.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# ===========================================================================
# Enums
# ===========================================================================

class AssessmentStatus(str, PyEnum):
    pending = "pending"
    processing = "processing"
    complete = "complete"
    failed = "failed"


# ===========================================================================
# ORM Models
# ===========================================================================

class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum(AssessmentStatus, name="assessment_status"),
        nullable=False,
        default=AssessmentStatus.pending,
    )
    risk_score: Mapped[int] = mapped_column(Integer, default=0)
    risk_classification: Mapped[str] = mapped_column(String(64), default="UNKNOWN")
    pcap_filename: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    config_filename: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    vendor: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    ike_version: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    exchange_type: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    critical_violations: Mapped[int] = mapped_column(Integer, default=0)
    high_violations: Mapped[int] = mapped_column(Integer, default=0)
    medium_violations: Mapped[int] = mapped_column(Integer, default=0)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    findings: Mapped[List["Finding"]] = relationship(
        "Finding", back_populates="assessment", cascade="all, delete-orphan"
    )
    pq_result: Mapped[Optional["PQResult"]] = relationship(
        "PQResult", back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
    esp_result: Mapped[Optional["ESPResult"]] = relationship(
        "ESPResult", back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )
    report_hash: Mapped[Optional["ReportHash"]] = relationship(
        "ReportHash", back_populates="assessment", uselist=False, cascade="all, delete-orphan"
    )


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )
    rule_id: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    standard: Mapped[str] = mapped_column(String(256), nullable=False)
    violation: Mapped[str] = mapped_column(Text, nullable=False)
    impact: Mapped[str] = mapped_column(Text, nullable=False)
    remediation_goal: Mapped[str] = mapped_column(Text, nullable=False)

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="findings")


class PQResult(Base):
    __tablename__ = "pq_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    qtei_score: Mapped[float] = mapped_column(Float, default=0.0)
    threat_classification: Mapped[str] = mapped_column(String(64), default="UNKNOWN")
    hndl_risk_window: Mapped[str] = mapped_column(String(128), default="Unknown")
    shor_vulnerable: Mapped[bool] = mapped_column(Boolean, default=False)
    grover_assessment: Mapped[str] = mapped_column(Text, default="")
    defense_action: Mapped[str] = mapped_column(Text, default="")

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="pq_result")


class ESPResult(Base):
    __tablename__ = "esp_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    inferred_cipher: Mapped[str] = mapped_column(String(128), default="Unknown")
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    entropy: Mapped[float] = mapped_column(Float, default=0.0)
    icv_bits: Mapped[int] = mapped_column(Integer, default=0)
    operational_mode: Mapped[str] = mapped_column(String(64), default="Unknown")

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="esp_result")


class ReportHash(Base):
    __tablename__ = "report_hashes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    anchored_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="report_hash")


# ===========================================================================
# Pydantic Response Schemas
# ===========================================================================

class FindingResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    rule_id: str
    severity: str
    standard: str
    violation: str
    impact: str
    remediation_goal: str

    model_config = {"from_attributes": True}


class PQResultResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    qtei_score: float
    threat_classification: str
    hndl_risk_window: str
    shor_vulnerable: bool
    grover_assessment: str
    defense_action: str

    model_config = {"from_attributes": True}


class ESPResultResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    inferred_cipher: str
    confidence_score: float
    entropy: float
    icv_bits: int
    operational_mode: str

    model_config = {"from_attributes": True}


class ReportHashResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    sha256_hash: str
    anchored_at: datetime

    model_config = {"from_attributes": True}


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    user_id: str
    name: str
    status: str
    risk_score: int
    risk_classification: str
    pcap_filename: Optional[str] = None
    config_filename: Optional[str] = None
    vendor: Optional[str] = None
    ike_version: Optional[str] = None
    exchange_type: Optional[str] = None
    critical_violations: int
    high_violations: int
    medium_violations: int
    created_at: datetime
    updated_at: datetime
    findings: List[FindingResponse] = Field(default_factory=list)
    pq_result: Optional[PQResultResponse] = None
    esp_result: Optional[ESPResultResponse] = None
    report_hash: Optional[ReportHashResponse] = None

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_assessments: int
    critical_count: int
    high_count: int
    avg_risk_score: float
    recent_assessments: List[Dict[str, Any]] = Field(default_factory=list)
    severity_distribution: Dict[str, int] = Field(default_factory=dict)
    vendor_distribution: Dict[str, int] = Field(default_factory=dict)
