"""Initial schema — all tables from data-model.md + ADR-002.

Revision ID: 001
Revises:
Create Date: 2026-06-11
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None

_AUDIT = [
    sa.Column("id", sa.String(36), primary_key=True),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("created_by", sa.String(36), nullable=True),
    sa.Column("updated_by", sa.String(36), nullable=True),
]


def upgrade() -> None:
    # organizations — no FK deps
    op.create_table(
        "organizations",
        *_AUDIT,
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("slug", sa.Text(), nullable=False),
        sa.Column("edition", sa.Text(), nullable=False, server_default="co_worker"),
        sa.Column("region", sa.Text(), nullable=False),
        sa.Column("sso_config", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False, server_default="active"),
    )
    op.create_index("ix_organizations_slug", "organizations", ["slug"], unique=True)

    # curricula — no FK deps (must precede cohorts)
    op.create_table(
        "curricula",
        *_AUDIT,
        sa.Column("edition", sa.Text(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("version", sa.Text(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="draft"),
    )

    # users — FK → organizations
    op.create_table(
        "users",
        *_AUDIT,
        sa.Column("organization_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("auth_provider", sa.Text(), nullable=False),
        sa.Column("external_subject", sa.Text(), nullable=True),
        sa.Column("password_hash", sa.Text(), nullable=True),
        sa.Column("global_role", sa.Text(), nullable=False, server_default="learner"),
        sa.Column("status", sa.Text(), nullable=False, server_default="invited"),
        sa.UniqueConstraint("organization_id", "email", name="uq_user_org_email"),
    )
    op.create_index("ix_users_external_subject", "users", ["external_subject"])

    # cohorts — FK → organizations, curricula
    op.create_table(
        "cohorts",
        *_AUDIT,
        sa.Column("organization_id", sa.String(36), sa.ForeignKey("organizations.id"), nullable=False),
        sa.Column("curriculum_id", sa.String(36), sa.ForeignKey("curricula.id"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("starts_on", sa.Text(), nullable=True),
        sa.Column("ends_on", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False, server_default="draft"),
    )

    # enrolments — FK → cohorts, users
    op.create_table(
        "enrolments",
        *_AUDIT,
        sa.Column("cohort_id", sa.String(36), sa.ForeignKey("cohorts.id"), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.Text(), nullable=False, server_default="learner"),
        sa.Column("status", sa.Text(), nullable=False, server_default="active"),
        sa.UniqueConstraint("cohort_id", "user_id", name="uq_enrolment_cohort_user"),
    )

    # modules — FK → curricula
    op.create_table(
        "modules",
        *_AUDIT,
        sa.Column("curriculum_id", sa.String(36), sa.ForeignKey("curricula.id"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("summary_markdown", sa.Text(), nullable=True),
    )

    # exercises — FK → modules
    op.create_table(
        "exercises",
        *_AUDIT,
        sa.Column("module_id", sa.String(36), sa.ForeignKey("modules.id"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("sequence_index", sa.Integer(), nullable=False),
        sa.Column("prompt_markdown", sa.Text(), nullable=False),
        sa.Column("build_spec", sa.Text(), nullable=False),
        sa.Column("prerequisite_exercise_ids", sa.Text(), nullable=True),
        sa.Column("min_attempts", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("min_distinct_approaches", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("min_exploration_seconds", sa.Integer(), nullable=False, server_default="300"),
        sa.Column("allow_fast_unlock", sa.Boolean(), nullable=False, server_default="true"),
    )

    # scenarios — FK → exercises
    op.create_table(
        "scenarios",
        *_AUDIT,
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("input_payload", sa.Text(), nullable=False),
        sa.Column("assertions", sa.Text(), nullable=False),
        sa.Column("weight", sa.Numeric(), nullable=False, server_default="1.0"),
    )

    # rubric_criteria — FK → exercises
    op.create_table(
        "rubric_criteria",
        *_AUDIT,
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("weight", sa.Numeric(), nullable=False, server_default="1.0"),
        sa.Column("guidance_markdown", sa.Text(), nullable=True),
    )

    # approach_taxonomies — FK → exercises
    op.create_table(
        "approach_taxonomies",
        *_AUDIT,
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("label", sa.Text(), nullable=False),
        sa.Column("is_canonical", sa.Boolean(), nullable=False, server_default="false"),
    )

    # consolidation_contents — FK → exercises (one-to-one)
    op.create_table(
        "consolidation_contents",
        *_AUDIT,
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), unique=True, nullable=False),
        sa.Column("body_markdown", sa.Text(), nullable=False),
        sa.Column("reference_build", sa.Text(), nullable=True),
        sa.Column("check_questions", sa.Text(), nullable=True),
    )

    # exercise_progress — FK → enrolments, exercises
    op.create_table(
        "exercise_progress",
        *_AUDIT,
        sa.Column("enrolment_id", sa.String(36), sa.ForeignKey("enrolments.id"), nullable=False),
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("phase", sa.Text(), nullable=False, server_default="not_started"),
        sa.Column("attempts_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("attempts_genuine", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("distinct_approaches", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("exploration_seconds", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("explored", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("unlocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("mastery_score", sa.Numeric(), nullable=True),
        sa.Column("facilitator_override", sa.Text(), nullable=True),
        sa.UniqueConstraint("enrolment_id", "exercise_id", name="uq_progress_enrolment_exercise"),
    )

    # submissions — FK → exercise_progress, enrolments, exercises
    op.create_table(
        "submissions",
        *_AUDIT,
        sa.Column("exercise_progress_id", sa.String(36), sa.ForeignKey("exercise_progress.id"), nullable=False),
        sa.Column("enrolment_id", sa.String(36), sa.ForeignKey("enrolments.id"), nullable=False),
        sa.Column("exercise_id", sa.String(36), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("artifact_refs", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), nullable=False, server_default="queued"),
        sa.Column("idempotency_key", sa.Text(), unique=True, nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_submissions_exercise_enrolment", "submissions", ["exercise_id", "enrolment_id"])

    # evaluation_results — FK → submissions (one-to-one)
    op.create_table(
        "evaluation_results",
        *_AUDIT,
        sa.Column("submission_id", sa.String(36), sa.ForeignKey("submissions.id"), unique=True, nullable=False),
        sa.Column("schema_version", sa.Text(), nullable=False, server_default="1.0"),
        sa.Column("ran", sa.Boolean(), nullable=False),
        sa.Column("scenario_results", sa.Text(), nullable=True),
        sa.Column("rubric_scores", sa.Text(), nullable=True),
        sa.Column("overall_score", sa.Numeric(), nullable=False),
        sa.Column("productive_failure_signal", sa.Text(), nullable=False),
        sa.Column("detected_approach", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("feedback_markdown", sa.Text(), nullable=True),
        sa.Column("feedback_artifact_ref", sa.Text(), nullable=True),
        sa.Column("judge_model", sa.Text(), nullable=False),
        sa.Column("judge_escalated", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("usage_input_tokens", sa.Integer(), nullable=True),
        sa.Column("usage_output_tokens", sa.Integer(), nullable=True),
        sa.Column("usage_cache_read_tokens", sa.Integer(), nullable=True),
        sa.Column("cost_micro_usd", sa.Integer(), nullable=True),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("evaluation_results")
    op.drop_index("ix_submissions_exercise_enrolment", table_name="submissions")
    op.drop_table("submissions")
    op.drop_table("exercise_progress")
    op.drop_table("consolidation_contents")
    op.drop_table("approach_taxonomies")
    op.drop_table("rubric_criteria")
    op.drop_table("scenarios")
    op.drop_table("exercises")
    op.drop_table("modules")
    op.drop_table("enrolments")
    op.drop_table("cohorts")
    op.drop_index("ix_users_external_subject", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_organizations_slug", table_name="organizations")
    op.drop_table("curricula")
    op.drop_table("organizations")
