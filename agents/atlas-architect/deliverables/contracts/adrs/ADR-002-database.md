# ADR-002 — Datastore Choice

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Related:** [[ADR-001-tech-stack]], [[ADR-005-service-decomposition]], data-model.md

## Context

The Co-Worker pilot must persist: organizations/cohorts/users (corporate B2B), curriculum content (modules, exercises, problems, consolidation material), learner **progress and PF phase state**, **agent-build submissions** (semi-structured: prompts + config + small code + metadata), and **evaluation results** (rubric scores + judge feedback + detected approaches + token usage).

Forces:
- The **core learning loop is relational and transactional**: a learner's progress, attempts, and PF phase must update atomically. Strong consistency here is non-negotiable (gating correctness).
- **Submissions and evaluation results are semi-structured** and evolve as the rubric DSL evolves — flexible nested payloads beat rigid columns.
- **Submission artifacts** (uploaded files, larger code bundles) are blobs, not rows.
- **Hot, ephemeral state** (queue, sessions, rubric-prefix cache hints, rate limits) needs a fast KV store.
- MY/SG **data-residency**: a single managed Postgres in an approved region is simpler to attest than a polyglot spread.

## Decision

**PostgreSQL 16 as the system of record**, with **JSONB** for semi-structured payloads, **Redis** for ephemeral/hot state and the job queue, and an **S3-compatible object store** for artifacts.

| Store | Holds | Why |
|-------|-------|-----|
| **PostgreSQL 16** | Orgs, cohorts, users, memberships, modules, exercises, enrolments, progress, PF phase state, submissions (metadata + JSONB payload), evaluation results (JSONB scores) | One transactional core for the learning loop. JSONB gives schema flexibility for submission/rubric/result shapes without migrations per rubric tweak. Relational integrity for the gating-critical tables. |
| **Redis** | Job queue (evaluation requests), short-lived sessions, idempotency keys, rate limits | Fast KV; already the queue broker (RQ/Celery) per [[ADR-001-tech-stack]]. **Never the source of truth.** |
| **S3-compatible object store** | Submission file artifacts, generated evaluation report files (e.g. DOCX/PDF feedback), large agent-build bundles | Blobs don't belong in rows; object store is cheap and content-addressable. DB stores the pointer + checksum. |

### Conventions (locked)
- **UUIDv7** primary keys (time-sortable) on all entities.
- **JSONB columns are versioned**: every JSONB payload carries a `schema_version` field so we can evolve the rubric/result/submission shapes safely.
- **No cross-module foreign keys that violate the ownership boundary** in [[ADR-005-service-decomposition]] — modules reference each other by ID + published service, not by reaching into another module's tables.
- **Soft-delete + audit columns** (`created_at`, `updated_at`, `deleted_at`, actor) on all top-level entities — corporate/grant auditability.
- **Token-usage accounting** is a typed column set on `EvaluationResult` (input/output/cache-read tokens, model, cost estimate) — LLM spend is a first-class, queryable cost.

## Consequences

**Positive**
- Single transactional system of record keeps PF gating correct and easy to reason about.
- JSONB absorbs the evolving submission/rubric/result shapes without a migration treadmill, while indexed columns stay queryable.
- Object store keeps the DB lean and artifacts cheap.

**Negative**
- JSONB flexibility can hide schema drift; mitigated by the mandatory `schema_version` field + validation at the API boundary (Pydantic models).
- Three stores to operate. Acceptable: Postgres + Redis + object store is a conventional, low-surface trio (and Redis/object-store are managed).

**Neutral**
- No search engine (Elasticsearch) or analytics warehouse in the pilot. Postgres full-text + JSONB queries suffice; revisit if cohort analytics outgrow it.
- No separate vector DB: the evaluator's LLM-judge does not require retrieval at pilot scale. If RAG enters the rubric later, add `pgvector` to the existing Postgres before introducing a new store.
