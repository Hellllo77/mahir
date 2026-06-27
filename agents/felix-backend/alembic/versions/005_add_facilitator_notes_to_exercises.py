"""Add facilitator_notes_markdown column to exercises.

Revision ID: 005
Revises: 004
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "exercises",
        sa.Column("facilitator_notes_markdown", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("exercises", "facilitator_notes_markdown")
