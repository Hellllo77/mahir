"""Individual-first pivot: user_curriculum table + user_id on exercise_progress.

Revision ID: 006
Revises: 005
Create Date: 2026-06-27
"""
from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # user_curricula — direct user→curriculum assignment (no cohort required)
    op.create_table(
        "user_curricula",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("updated_by", sa.String(36), nullable=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("curriculum_id", sa.String(36), sa.ForeignKey("curricula.id"), nullable=False),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "curriculum_id", name="uq_user_curriculum"),
    )
    op.create_index("ix_user_curricula_user_id", "user_curricula", ["user_id"])

    # exercise_progress: add user_id column + index
    op.add_column(
        "exercise_progress",
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
    )
    op.create_index("ix_exercise_progress_user_id", "exercise_progress", ["user_id"])

    # Backfill user_id from enrolments (keep only the most-recent record per user+exercise pair)
    op.execute(
        """
        UPDATE exercise_progress ep
        SET user_id = e.user_id
        FROM enrolments e
        WHERE ep.enrolment_id = e.id
          AND ep.user_id IS NULL
        """
    )


def downgrade() -> None:
    op.drop_index("ix_exercise_progress_user_id", table_name="exercise_progress")
    op.drop_column("exercise_progress", "user_id")
    op.drop_index("ix_user_curricula_user_id", table_name="user_curricula")
    op.drop_table("user_curricula")
