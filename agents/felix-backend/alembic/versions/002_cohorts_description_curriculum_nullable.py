"""Cohorts — add description column, make curriculum_id nullable.

Revision ID: 002
Revises: 001
Create Date: 2026-06-26
"""
from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cohorts", sa.Column("description", sa.Text(), nullable=True))
    op.alter_column("cohorts", "curriculum_id", existing_type=sa.String(36), nullable=True)


def downgrade() -> None:
    op.alter_column("cohorts", "curriculum_id", existing_type=sa.String(36), nullable=False)
    op.drop_column("cohorts", "description")
