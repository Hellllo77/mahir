"""Convert all native PG ENUM columns to TEXT — aligns DB schema with ORM native_enum=False.

Prior to this migration, staging PostgreSQL had native PG ENUM types on several columns
(cohortstatus, userstatus, etc.). The ORM was updated to native_enum=False in 55a67cf,
which causes asyncpg to send parameters as text without ::typename casts. PostgreSQL
cannot implicitly cast text parameters to native ENUM types in parameterized queries,
causing type-mismatch errors on INSERT/UPDATE.

This migration:
  1. ALTERs all affected columns TYPE to TEXT (idempotent — safe on already-TEXT columns)
  2. DROPs column DEFAULTs that reference the PG ENUM type (::typename cast in default)
  3. DROPs the now-unreferenced PG ENUM types (IF EXISTS — safe if never existed)
  4. Restores plain-text DEFAULTs on the affected columns

Order is critical: DROP TYPE fails while any column DEFAULT still references the type.
DROP DEFAULT must come BEFORE DROP TYPE.

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
    # Step 1: Convert all Enum columns to TEXT
    # (USING status::text works for both existing ENUM and TEXT columns)
    op.execute("ALTER TABLE organizations ALTER COLUMN edition TYPE text USING edition::text")
    op.execute("ALTER TABLE organizations ALTER COLUMN status TYPE text USING status::text")

    op.execute("ALTER TABLE users ALTER COLUMN auth_provider TYPE text USING auth_provider::text")
    op.execute("ALTER TABLE users ALTER COLUMN global_role TYPE text USING global_role::text")
    op.execute("ALTER TABLE users ALTER COLUMN status TYPE text USING status::text")

    op.execute("ALTER TABLE cohorts ALTER COLUMN status TYPE text USING status::text")

    op.execute("ALTER TABLE enrolments ALTER COLUMN role TYPE text USING role::text")
    op.execute("ALTER TABLE enrolments ALTER COLUMN status TYPE text USING status::text")

    op.execute("ALTER TABLE curricula ALTER COLUMN status TYPE text USING status::text")
    op.execute("ALTER TABLE exercise_progress ALTER COLUMN phase TYPE text USING phase::text")
    op.execute("ALTER TABLE submissions ALTER COLUMN status TYPE text USING status::text")

    # Step 2: Drop DEFAULTs that reference the PG ENUM types via ::typename cast.
    # PostgreSQL refuses DROP TYPE while any column DEFAULT still references the type.
    # These DEFAULTs are re-added as plain-text in Step 4.
    # (DROP DEFAULT is a no-op if the column has no default — safe on fresh DBs.)
    op.execute("ALTER TABLE cohorts ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TABLE enrolments ALTER COLUMN role DROP DEFAULT")
    op.execute("ALTER TABLE enrolments ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TABLE organizations ALTER COLUMN edition DROP DEFAULT")
    op.execute("ALTER TABLE organizations ALTER COLUMN status DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN global_role DROP DEFAULT")
    op.execute("ALTER TABLE users ALTER COLUMN status DROP DEFAULT")

    # Step 3: Drop the PG ENUM types (IF EXISTS — safe if they were never created)
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

    # Step 4: Restore plain-text DEFAULTs (no ::typename cast — pure text literals)
    op.execute("ALTER TABLE cohorts ALTER COLUMN status SET DEFAULT 'draft'")
    op.execute("ALTER TABLE enrolments ALTER COLUMN role SET DEFAULT 'learner'")
    op.execute("ALTER TABLE enrolments ALTER COLUMN status SET DEFAULT 'active'")
    op.execute("ALTER TABLE organizations ALTER COLUMN edition SET DEFAULT 'co_worker'")
    op.execute("ALTER TABLE organizations ALTER COLUMN status SET DEFAULT 'active'")
    op.execute("ALTER TABLE users ALTER COLUMN global_role SET DEFAULT 'learner'")
    op.execute("ALTER TABLE users ALTER COLUMN status SET DEFAULT 'invited'")


def downgrade() -> None:
    # No downgrade — reverting to native ENUM columns would require knowing which types
    # existed on each deployment, recreating them, and restoring ::typename defaults.
    # This is a one-way schema normalisation migration.
    pass
