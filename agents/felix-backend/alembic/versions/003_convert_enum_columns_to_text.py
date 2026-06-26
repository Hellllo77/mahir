"""Convert all native PG ENUM columns to TEXT — aligns DB schema with ORM native_enum=False.

Prior to this migration, staging PostgreSQL had native PG ENUM types on several columns
(cohortstatus, userstatus, etc.). The ORM was updated to native_enum=False in 55a67cf,
which causes asyncpg to send parameters as text without ::typename casts. PostgreSQL
cannot implicitly cast text parameters to native ENUM types in parameterized queries,
causing UndefinedObject or type-mismatch errors on INSERT/UPDATE.

This migration ALTERs all affected columns to TEXT and drops the now-unused PG ENUM types.
Safe to run on DBs that already have TEXT columns — ALTER COLUMN ... TYPE text is idempotent.

Revision ID: 003
Revises: 002
Create Date: 2026-06-27
"""
from alembic import op

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # organizations
    op.execute("ALTER TABLE organizations ALTER COLUMN edition TYPE text USING edition::text")
    op.execute("ALTER TABLE organizations ALTER COLUMN status TYPE text USING status::text")

    # users
    op.execute("ALTER TABLE users ALTER COLUMN auth_provider TYPE text USING auth_provider::text")
    op.execute("ALTER TABLE users ALTER COLUMN global_role TYPE text USING global_role::text")
    op.execute("ALTER TABLE users ALTER COLUMN status TYPE text USING status::text")

    # cohorts
    op.execute("ALTER TABLE cohorts ALTER COLUMN status TYPE text USING status::text")

    # enrolments
    op.execute("ALTER TABLE enrolments ALTER COLUMN role TYPE text USING role::text")
    op.execute("ALTER TABLE enrolments ALTER COLUMN status TYPE text USING status::text")

    # curricula
    op.execute("ALTER TABLE curricula ALTER COLUMN status TYPE text USING status::text")

    # exercise_progress
    op.execute("ALTER TABLE exercise_progress ALTER COLUMN phase TYPE text USING phase::text")

    # submissions
    op.execute("ALTER TABLE submissions ALTER COLUMN status TYPE text USING status::text")

    # Drop PG ENUM types if they exist (created by native_enum=True ORM, not used by migrations)
    op.execute("DROP TYPE IF EXISTS cohortstatus")
    op.execute("DROP TYPE IF EXISTS orgstatus")
    op.execute("DROP TYPE IF EXISTS orgedition")
    op.execute("DROP TYPE IF EXISTS userauthprovider")
    op.execute("DROP TYPE IF EXISTS userglobalrole")
    op.execute("DROP TYPE IF EXISTS userstatus")
    op.execute("DROP TYPE IF EXISTS enrolmentrole")
    op.execute("DROP TYPE IF EXISTS enrolmentstatus")
    op.execute("DROP TYPE IF EXISTS curriculumstatus")
    op.execute("DROP TYPE IF EXISTS exercisephase")
    op.execute("DROP TYPE IF EXISTS submissionstatus")


def downgrade() -> None:
    # No downgrade — reverting to native ENUM columns would require knowing which types
    # existed on each deployment and recreating them. Treat this as a one-way migration.
    pass
