# Test Pyramid — Mahir Co-Worker Pilot

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** vera-qa-mahir
- **Task:** T-005
- **Related:** [[mahir-api.yaml]], [[evaluation-events.md]], [[ADR-003-evaluator-design]], [[ADR-004-productive-failure-sequencing]]

---

## Overview

Five layers. Each layer tests what the layer below cannot: no duplication between layers is intentional — the pyramid is not a checklist of repeated scenarios.

```
           ┌──────────────────────────────┐
           │     E2E (Playwright)  ≤5     │  full-stack critical paths
           ├──────────────────────────────┤
           │      Realtime / Events       │  evaluation event lifecycle
           ├──────────────────────────────┤
           │    Isolation / Multi-tenant  │  row-level tenant boundary matrix
           ├──────────────────────────────┤
           │    Integration (HTTP layer)  │  one spec per route group
           ├──────────────────────────────┤
           │    Unit (service + schema)   │  PF gate logic, sandbox, judge schemas
           └──────────────────────────────┘
```

---

## Layer Definitions

### Unit
**Scope:** Pure functions, service-layer logic, schema validation — no HTTP, no I/O.  
**Files:** `agents/felix-backend/tests/test_progress.py`, `test_evaluator.py`, `test_auth.py` (JWT/hash helpers)  
**Naming:** `test_<unit>_<condition>` — e.g. `test_gate_opens_after_two_genuine_attempts`

### Integration (HTTP layer)
**Scope:** HTTPX `AsyncClient` over ASGI transport; exercises every route in `mahir-api.yaml`; no real Redis or LLM calls (queue + judge are dependency-injected or patched).  
**Files:** `agents/felix-backend/tests/test_auth.py`, `test_curriculum.py`, `test_submissions.py`, `test_http_progress.py`  
**Naming:** `test_<verb>_<resource>_<condition>` — e.g. `test_get_progress_unauthenticated_returns_403`  
**Fixture strategy:** Transaction-rollback per test (see Isolation Pattern below).

### Isolation (Multi-tenant)
**Scope:** N roles × M resource types per org-scoped table. Every check is a cross-org access attempt that MUST return 403 or 404.  
**Files:** `agents/felix-backend/tests/test_tenant_isolation.py`  
**Naming:** `test_<subject>_cannot_<action>_<object>` — e.g. `test_learner_cannot_access_other_org_cohort_modules`  
**Matrix:** see §Isolation Matrix below.

### Realtime / Events
**Scope:** Evaluation event lifecycle — status transitions driven by the async evaluator pipeline (ADR-003/ADR-005); idempotency of `event_id` deduplication; PF gate triggered only by `evaluation.completed` (not `evaluation.failed`).  
**Files:** `agents/felix-backend/tests/test_realtime_events.py`  
**Naming:** `test_evaluation_<event_type>_<condition>`

### E2E (Playwright)
**Scope:** Critical paths where failure means lost access, revenue, or data that only the full stack can catch. Maximum 5 specs. Runs against live local dev stack (`http://localhost:3000` frontend, `http://localhost:8000` backend).  
**Files:** `agents/vera-qa/tests/e2e/`  
**Config:** `agents/vera-qa/playwright.config.ts`  
**Naming:** `<flow>.spec.ts` — e.g. `learner-submit-flow.spec.ts`

---

## Isolation Pattern

All backend tests use **transaction-rollback isolation** (ADR-002 §testing): each test runs inside an open DB transaction that is rolled back at teardown. No test data persists between tests.

```python
# conftest.py — established by felix-backend
@pytest_asyncio.fixture
async def db(create_tables) -> AsyncGenerator[AsyncSession, None]:
    async with _test_engine.connect() as conn:
        await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await conn.rollback()
```

All fixtures (org, learner, cohort, enrolment, exercise, progress) compose on top of this session. Test code calls `db.flush()` to materialise IDs without committing.

---

## Fixture Strategy

| Fixture | What it creates | Scope |
|---------|----------------|-------|
| `org` | `Organization` (Org A, `test-corp`) | function |
| `org2` / `org_b` | `Organization` (Org B — isolation tests) | function |
| `curriculum` | `Curriculum` (co_worker, published) | function |
| `module` | `Module` in curriculum | function |
| `exercise` | `Exercise` with PF gate (min_attempts=2, min_distinct_approaches=2, min_exploration_seconds=300, allow_fast_unlock=True) | function |
| `learner` | `User` (global_role=learner) in Org A | function |
| `facilitator` | `User` (global_role=facilitator) in Org A | function |
| `cohort` | `Cohort` (running) in Org A | function |
| `enrolment` | `Enrolment` of learner in cohort | function |
| `progress` | `ExerciseProgress` (phase=exploring) for enrolment+exercise | function |

Helper `make_auth_header(user)` produces a valid Bearer token without hitting the DB.

---

## Isolation Matrix

| Action | Subject | Object | Expected |
|--------|---------|--------|----------|
| GET cohort modules | Learner (Org A) | Cohort (Org B) | 403 or 404 |
| GET submission | Learner (Org B) | Submission (Org A) | 403 or 404 |
| POST facilitator override | Facilitator (Org A) | Progress (Org B) | 403 or 404 |
| GET exercise progress | Learner (Org A) | Progress (Org B enrolment) | 403 or 404 |
| GET cohort roster | Facilitator (Org A) | Cohort (Org B) | 403 or 404 |
| GET submission list | Learner (Org A) | Submissions (Org B exercise) | 200 empty or 403/404 |

---

## Environment Variables

| Variable | Required for | Default |
|----------|-------------|---------|
| `TEST_DATABASE_URL` | backend unit/integration/isolation | derived from `DATABASE_URL` (replaces `/mahir` → `/mahir_test`) |
| `DATABASE_URL` | backend | `postgresql+asyncpg://postgres:postgres@localhost:5432/mahir` |
| `SECRET_KEY` | JWT signing | `dev-secret-key` |
| `ANTHROPIC_API_KEY` | judge tests (skipped if absent) | absent in CI → judge tests skip |
| `REDIS_URL` | RQ queue (mocked/skipped in unit tests) | `redis://localhost:6379/0` |
| `NEXT_PUBLIC_API_BASE` | E2E frontend → backend URL | `http://localhost:8000/v1` |
| `PLAYWRIGHT_BASE_URL` | E2E frontend | `http://localhost:3000` |

---

## Known Issues (Blocking — Pilot Go-Live)

### BUG-001 — `/me/progress` query parameter mismatch
- **Severity:** BLOCKING
- **Layer:** Integration (frontend → backend)
- **Description:** `frontend/src/lib/api-client.ts:145` sends `?enrolmentId=` (camelCase) but `agents/felix-backend/src/progress/router.py:13` declares `enrolment_id: str = Query(...)` (snake_case). FastAPI will return 422 for every call to `GET /me/progress` from the frontend.
- **Contract:** `mahir-api.yaml` declares `name: enrolmentId` for the query param — the **backend** is out of contract; the frontend is correct.
- **Fix:** Add `alias="enrolmentId"` to the FastAPI `Query(...)` in `progress/router.py`, or rename the Python param to match.
- **Test:** `test_get_my_progress_camelcase_param` in `test_http_progress.py` documents and will catch any regression.

---

## CI Integration

Backend tests:
```bash
cd agents/felix-backend
pytest tests/ -x --tb=short
```

E2E (requires live stack):
```bash
cd agents/vera-qa
npx playwright test tests/e2e/
```
