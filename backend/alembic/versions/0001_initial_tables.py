"""Initial tables

Revision ID: 0001
Revises: 
Create Date: 2026-09-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'assessments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.String(255), nullable=False, index=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('risk_score', sa.Integer(), nullable=True),
        sa.Column('risk_classification', sa.String(50), nullable=True),
        sa.Column('pcap_filename', sa.String(500), nullable=True),
        sa.Column('config_filename', sa.String(500), nullable=True),
        sa.Column('vendor', sa.String(100), nullable=True),
        sa.Column('ike_version', sa.String(50), nullable=True),
        sa.Column('exchange_type', sa.String(200), nullable=True),
        sa.Column('critical_violations', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('high_violations', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('medium_violations', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'findings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False),
        sa.Column('rule_id', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('standard', sa.String(200), nullable=True),
        sa.Column('violation', sa.Text(), nullable=False),
        sa.Column('impact', sa.Text(), nullable=True),
        sa.Column('remediation_goal', sa.Text(), nullable=True),
    )
    op.create_index('ix_findings_assessment_id', 'findings', ['assessment_id'])

    op.create_table(
        'pq_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('qtei_score', sa.Float(), nullable=True),
        sa.Column('threat_classification', sa.String(100), nullable=True),
        sa.Column('hndl_risk_window', sa.String(200), nullable=True),
        sa.Column('shor_vulnerable', sa.Boolean(), nullable=True),
        sa.Column('grover_assessment', sa.Text(), nullable=True),
        sa.Column('defense_action', sa.Text(), nullable=True),
        sa.Column('target_cipher', sa.String(200), nullable=True),
        sa.Column('estimated_qubits', sa.String(200), nullable=True),
    )

    op.create_table(
        'esp_results',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('inferred_cipher', sa.String(100), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('entropy', sa.Float(), nullable=True),
        sa.Column('icv_bits', sa.Integer(), nullable=True),
        sa.Column('operational_mode', sa.String(100), nullable=True),
        sa.Column('mode_confidence', sa.Float(), nullable=True),
    )

    op.create_table(
        'report_hashes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('assessment_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('assessments.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('sha256_hash', sa.String(64), nullable=False),
        sa.Column('anchored_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('report_hashes')
    op.drop_table('esp_results')
    op.drop_table('pq_results')
    op.drop_table('findings')
    op.drop_table('assessments')
