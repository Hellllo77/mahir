"""Test infrastructure — transaction-rollback isolation (ADR-002 §testing)."""
import asyncio
import json
from datetime import datetime, timezone
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from src.config import settings
from src.db.base import Base
from src.db.models.auth import (
    Enrolment, EnrolmentRole, Organization, User, UserAuthProvider,
    UserGlobalRole, Cohort, CohortStatus
)
from src.db.models.curriculum import (
    Curriculum, CurriculumEdition, CurriculumStatus,
    Exercise, Module, RubricCriterion, Scenario, ApproachTaxonomy
)
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.models.submission import Submission, SubmissionStatus
from src.db.uuidv7 import uuid7_str
from src.lib.jwt import create_access_token, hash_password
from src.main import app

# Use a separate test DB URL (override via TEST_DATABASE_URL env var)
TEST_DB_URL = settings.database_url.replace("/mahir", "/mahir_test")

_test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
_TestSessionLocal = async_sessionmaker(_test_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def create_tables():
    """Create test schema synchronously (psycopg2) to avoid Python 3.14 event-loop issues."""
    import psycopg2
    from sqlalchemy import create_engine

    sync_url = TEST_DB_URL.replace("postgresql+asyncpg://", "postgresql://")
    sync_engine = create_engine(sync_url)
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.dispose()
    yield
    sync_engine2 = create_engine(sync_url)
    Base.metadata.drop_all(sync_engine2)
    sync_engine2.dispose()


@pytest_asyncio.fixture
async def db(create_tables) -> AsyncGenerator[AsyncSession, None]:
    """Transaction-rollback isolated session — each test gets a fresh rollback."""
    async with _test_engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await conn.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession):
    """HTTPX async client with DB session override.

    Routes live in the mounted v1 sub-app, so the override must be applied there,
    not only on the outer app.
    """
    from src.db.base import get_db
    from src.main import v1

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    v1.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()
    v1.dependency_overrides.clear()


# ── Fixture factories ───────────────────────────────────────────────────────


@pytest_asyncio.fixture
async def org(db: AsyncSession) -> Organization:
    o = Organization(
        id=uuid7_str(),
        name="Test Corp",
        slug="test-corp",
        edition="co_worker",
        region="ap-southeast-1",
    )
    db.add(o)
    await db.flush()
    return o


@pytest_asyncio.fixture
async def org2(db: AsyncSession) -> Organization:
    """Second org for tenant-isolation tests."""
    o = Organization(
        id=uuid7_str(),
        name="Other Corp",
        slug="other-corp",
        edition="co_worker",
        region="ap-southeast-1",
    )
    db.add(o)
    await db.flush()
    return o


@pytest_asyncio.fixture
async def curriculum(db: AsyncSession) -> Curriculum:
    c = Curriculum(
        id=uuid7_str(),
        edition=CurriculumEdition.co_worker,
        title="Agent Fundamentals",
        version="1.0",
        status=CurriculumStatus.published,
    )
    db.add(c)
    await db.flush()
    return c


@pytest_asyncio.fixture
async def module(db: AsyncSession, curriculum: Curriculum) -> Module:
    m = Module(
        id=uuid7_str(),
        curriculum_id=curriculum.id,
        title="Module 1",
        sequence_index=1,
    )
    db.add(m)
    await db.flush()
    return m


@pytest_asyncio.fixture
async def exercise(db: AsyncSession, module: Module) -> Exercise:
    e = Exercise(
        id=uuid7_str(),
        module_id=module.id,
        title="Build a simple classifier",
        sequence_index=1,
        prompt_markdown="Build an agent that classifies text as positive or negative.",
        build_spec=json.dumps({"schema_version": "1.0", "required_fields": ["model", "tools"]}),
        min_attempts=2,
        min_distinct_approaches=2,
        min_exploration_seconds=300,
        allow_fast_unlock=True,
    )
    db.add(e)
    await db.flush()
    return e


@pytest_asyncio.fixture
async def scenario(db: AsyncSession, exercise: Exercise) -> Scenario:
    s = Scenario(
        id=uuid7_str(),
        exercise_id=exercise.id,
        name="Basic sentiment",
        input_payload=json.dumps({"text": "I love this!"}),
        assertions=json.dumps({"checks": [{"field": "model", "expected": "claude-haiku-4-5"}]}),
        weight=1.0,
    )
    db.add(s)
    await db.flush()
    return s


@pytest_asyncio.fixture
async def rubric_criterion(db: AsyncSession, exercise: Exercise) -> RubricCriterion:
    c = RubricCriterion(
        id=uuid7_str(),
        exercise_id=exercise.id,
        code="tool.defined",
        description="Agent defines at least one tool",
        weight=1.0,
    )
    db.add(c)
    await db.flush()
    return c


def make_user(org: Organization, role: UserGlobalRole = UserGlobalRole.learner) -> User:
    import uuid
    from src.db.models.auth import UserStatus
    return User(
        id=uuid7_str(),
        organization_id=org.id,
        email=f"user-{uuid.uuid4().hex[:12]}@test.example",
        display_name="Test Learner",
        auth_provider=UserAuthProvider.local,
        password_hash=hash_password("password123"),
        global_role=role,
        status=UserStatus.active,
    )


@pytest_asyncio.fixture
async def learner(db: AsyncSession, org: Organization) -> User:
    u = make_user(org)
    db.add(u)
    await db.flush()
    return u


@pytest_asyncio.fixture
async def facilitator(db: AsyncSession, org: Organization) -> User:
    u = make_user(org, role=UserGlobalRole.facilitator)
    db.add(u)
    await db.flush()
    return u


@pytest_asyncio.fixture
async def cohort(db: AsyncSession, org: Organization, curriculum: Curriculum) -> Cohort:
    c = Cohort(
        id=uuid7_str(),
        organization_id=org.id,
        curriculum_id=curriculum.id,
        name="Cohort A",
        status=CohortStatus.running,
    )
    db.add(c)
    await db.flush()
    return c


@pytest_asyncio.fixture
async def enrolment(db: AsyncSession, cohort: Cohort, learner: User) -> Enrolment:
    e = Enrolment(
        id=uuid7_str(),
        cohort_id=cohort.id,
        user_id=learner.id,
        role=EnrolmentRole.learner,
    )
    db.add(e)
    await db.flush()
    return e


@pytest_asyncio.fixture
async def progress(db: AsyncSession, enrolment: Enrolment, exercise: Exercise) -> ExerciseProgress:
    p = ExerciseProgress(
        id=uuid7_str(),
        enrolment_id=enrolment.id,
        exercise_id=exercise.id,
        phase=ExercisePhase.exploring,
    )
    db.add(p)
    await db.flush()
    return p


def make_auth_header(user: User) -> dict:
    token, _ = create_access_token(user.id, user.organization_id, user.global_role.value)
    return {"Authorization": f"Bearer {token}"}
