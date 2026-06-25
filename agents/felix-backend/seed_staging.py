"""Staging seed — vera re-shakedown data. Run from app root: python seed_staging.py"""
import asyncio
import json

from sqlalchemy import select

from src.db.base import AsyncSessionLocal
from src.db.models.auth import Cohort, Enrolment, Organization, User
from src.db.models.curriculum import Curriculum, Exercise, Module
from src.db.uuidv7 import uuid7_str
from src.lib.jwt import hash_password

LEARNER1_EMAIL = "alice@mahir-pilot.com"
LEARNER1_PASS = "Alice123!"
LEARNER2_EMAIL = "bob@mahir-pilot.com"
LEARNER2_PASS = "Bob123!"


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        # Reuse existing org
        result = await db.execute(select(Organization).limit(1))
        org = result.scalar_one_or_none()
        if org is None:
            raise RuntimeError("No org found — run seed_admin.py first.")
        print(f"[seed] org  id={org.id} slug={org.slug}")

        # Curriculum
        result = await db.execute(
            select(Curriculum).where(Curriculum.deleted_at.is_(None)).limit(1)
        )
        curriculum = result.scalar_one_or_none()
        if curriculum is None:
            curriculum = Curriculum(
                id=uuid7_str(),
                edition="co_worker",
                title="Mahir Pilot Curriculum",
                version="1.0",
                status="published",
            )
            db.add(curriculum)
            await db.flush()
            print(f"[seed] created curriculum id={curriculum.id}")
        else:
            print(f"[seed] using curriculum   id={curriculum.id}")

        # Module
        result = await db.execute(
            select(Module)
            .where(Module.curriculum_id == curriculum.id, Module.deleted_at.is_(None))
            .limit(1)
        )
        module = result.scalar_one_or_none()
        if module is None:
            module = Module(
                id=uuid7_str(),
                curriculum_id=curriculum.id,
                title="Module 1 — Introduction to AI Agents",
                sequence_index=1,
                summary_markdown="Build your first AI agent using the Anthropic API.",
            )
            db.add(module)
            await db.flush()
            print(f"[seed] created module id={module.id}")
        else:
            print(f"[seed] using module   id={module.id}")

        # Exercise
        result = await db.execute(
            select(Exercise)
            .where(Exercise.module_id == module.id, Exercise.deleted_at.is_(None))
            .limit(1)
        )
        exercise = result.scalar_one_or_none()
        if exercise is None:
            build_spec = json.dumps({
                "schema_version": "1.0",
                "type": "agent_build",
                "description": "Build a simple agent that answers questions.",
            })
            exercise = Exercise(
                id=uuid7_str(),
                module_id=module.id,
                title="Exercise 1 — Simple Q&A Agent",
                sequence_index=1,
                prompt_markdown="Build an agent that uses Claude to answer user questions.",
                build_spec=build_spec,
                min_attempts=2,
                min_distinct_approaches=2,
                min_exploration_seconds=300,
                allow_fast_unlock=True,
            )
            db.add(exercise)
            await db.flush()
            print(f"[seed] created exercise id={exercise.id}")
        else:
            print(f"[seed] using exercise   id={exercise.id}")

        # Active cohort
        result = await db.execute(
            select(Cohort)
            .where(
                Cohort.organization_id == org.id,
                Cohort.curriculum_id == curriculum.id,
                Cohort.status == "running",
                Cohort.deleted_at.is_(None),
            )
            .limit(1)
        )
        cohort = result.scalar_one_or_none()
        if cohort is None:
            cohort = Cohort(
                id=uuid7_str(),
                organization_id=org.id,
                name="Pilot Cohort 1",
                curriculum_id=curriculum.id,
                starts_on="2026-06-25",
                status="running",
            )
            db.add(cohort)
            await db.flush()
            print(f"[seed] created cohort id={cohort.id}")
        else:
            print(f"[seed] using cohort   id={cohort.id}")

        # Learner 1 — enrolled
        result = await db.execute(
            select(User).where(User.email == LEARNER1_EMAIL, User.deleted_at.is_(None))
        )
        learner1 = result.scalar_one_or_none()
        if learner1 is None:
            learner1 = User(
                id=uuid7_str(),
                organization_id=org.id,
                email=LEARNER1_EMAIL,
                display_name="Alice",
                auth_provider="local",
                password_hash=hash_password(LEARNER1_PASS),
                global_role="learner",
                status="active",
            )
            db.add(learner1)
            await db.flush()
            print(f"[seed] created learner1 id={learner1.id}")
        else:
            print(f"[seed] using learner1   id={learner1.id}")

        # Enrolment for learner 1
        result = await db.execute(
            select(Enrolment).where(
                Enrolment.user_id == learner1.id,
                Enrolment.cohort_id == cohort.id,
                Enrolment.deleted_at.is_(None),
            )
        )
        if result.scalar_one_or_none() is None:
            enrolment = Enrolment(
                id=uuid7_str(),
                cohort_id=cohort.id,
                user_id=learner1.id,
                role="learner",
                status="active",
            )
            db.add(enrolment)
            print(f"[seed] enrolled learner1 in cohort {cohort.id}")
        else:
            print(f"[seed] learner1 already enrolled")

        # Learner 2 — no enrolment
        result = await db.execute(
            select(User).where(User.email == LEARNER2_EMAIL, User.deleted_at.is_(None))
        )
        learner2 = result.scalar_one_or_none()
        if learner2 is None:
            learner2 = User(
                id=uuid7_str(),
                organization_id=org.id,
                email=LEARNER2_EMAIL,
                display_name="Bob",
                auth_provider="local",
                password_hash=hash_password(LEARNER2_PASS),
                global_role="learner",
                status="active",
            )
            db.add(learner2)
            print(f"[seed] created learner2 id={learner2.id}")
        else:
            print(f"[seed] using learner2   id={learner2.id}")

        await db.commit()
        print("[seed] done.")
        print()
        print("=== STAGING LEARNER CREDENTIALS ===")
        print(f"Learner 1 (enrolled):     {LEARNER1_EMAIL} / {LEARNER1_PASS}")
        print(f"Learner 2 (no enrolment): {LEARNER2_EMAIL} / {LEARNER2_PASS}")


asyncio.run(seed())
