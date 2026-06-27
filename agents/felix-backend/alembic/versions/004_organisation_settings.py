"""Add organisation_settings table for per-org config (Resend API key etc).

Revision ID: 004
Revises: 003
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organisation_settings",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("org_id", sa.String(36), sa.ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("resend_api_key", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )
    op.create_index("ix_organisation_settings_org_id", "organisation_settings", ["org_id"])


def downgrade() -> None:
    op.drop_index("ix_organisation_settings_org_id", table_name="organisation_settings")
    op.drop_table("organisation_settings")
