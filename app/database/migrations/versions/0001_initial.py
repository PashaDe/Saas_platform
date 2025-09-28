"""initial core tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-09-28 00:00:00
"""

from alembic import op
import sqlalchemy as sa
import uuid
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("subdomain", sa.String(length=255), nullable=True, unique=True),
        sa.Column("plan_type", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="admin"),
        sa.Column("hashed_password", sa.String(length=255), nullable=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "provider_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("account_ref", sa.String(length=255), nullable=True),
        sa.Column("credentials_json", sa.JSON(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "export_configs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("filters_json", sa.JSON(), nullable=True),
        sa.Column("mapping_json", sa.JSON(), nullable=True),
        sa.Column("target_spreadsheet_id", sa.String(length=128), nullable=False),
        sa.Column("target_sheet", sa.String(length=128), nullable=False),
        sa.Column("write_strategy", sa.String(length=32), nullable=False, server_default="replace"),
        sa.Column("schedule_cron", sa.String(length=64), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "export_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("export_config_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("export_configs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="queued"),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("error_summary", sa.String(length=1000), nullable=True),
        sa.Column("records_read", sa.String(length=32), nullable=True),
        sa.Column("records_written", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_index("ix_export_tasks_company_status", "export_tasks", ["company_id", "status"]) 


def downgrade() -> None:
    op.drop_index("ix_export_tasks_company_status", table_name="export_tasks")
    op.drop_table("export_tasks")
    op.drop_table("export_configs")
    op.drop_table("provider_tokens")
    op.drop_table("users")
    op.drop_table("companies")


