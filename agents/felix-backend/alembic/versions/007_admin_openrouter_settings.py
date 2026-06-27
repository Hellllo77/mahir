"""Add openrouter_api_key + preferred_model to organisation_settings.

Revision ID: 007
Revises: 006
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "organisation_settings",
        sa.Column("openrouter_api_key", sa.String(), nullable=True),
    )
    op.add_column(
        "organisation_settings",
        sa.Column(
            "preferred_model",
            sa.String(),
            nullable=True,
            server_default="anthropic/claude-sonnet-4-6",
        ),
    )


def downgrade() -> None:
    op.drop_column("organisation_settings", "preferred_model")
    op.drop_column("organisation_settings", "openrouter_api_key")
