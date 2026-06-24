# ADR-001 — Technology Stack (Co-Worker Pilot)

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Supersedes:** —
- **Related:** [[ADR-002-database]], [[ADR-003-evaluator-design]], [[ADR-005-service-decomposition]]

## Context

Mahir teaches people to **build** AI agents via Productive Failure (PF). The grant-funded **Co-Worker (corporate)** edition is the pilot, targeting the MY/SG market. The mandate (per `DEFINITION.md`) is **curriculum-first**: prove the curriculum + evaluator in a live pilot before building a platform. No repository, staging, or deploy target is configured yet — this ADR defines the starting point.

Key forces:

1. **The evaluator must run learner-built AI agents.** Submissions are agent builds (prompts + config + small code). Grading combines deterministic scenario checks with an **LLM-judge**. The platform's own AI work is therefore Python/LLM-shaped.
2. **PF pedagogy** requires a stateful sequencing engine that gates consolidation content behind an exploration phase — server-authoritative, not client-trusted.
3. **Pilot scale is small** (cohorts of corporate learners, not millions). Optimize for iteration speed and low operational surface, not premature horizontal scale.
4. **Crew composition:** one backend dev (Sonnet tier), one frontend dev, one designer, one QA. The stack must be conventional enough for a small crew to move fast.
5. **Grant + corporate B2B** means data-residency sensitivity (MY/SG) and auditability matter early.

## Decision

Adopt a pragmatic, single-language-per-tier stack:

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Backend API + Curriculum Engine** | **Python 3.12 + FastAPI** | Async, first-class OpenAPI generation (aligns with our API contract), and the natural ecosystem for the LLM-judge evaluator. One language across API and evaluator reduces crew context-switching. |
| **Evaluator worker** | **Python 3.12** worker process, queue-driven | Shares models/domain code with the API. Runs sandboxed agent execution + LLM-judge. See [[ADR-003-evaluator-design]]. |
| **LLM-judge + agent runtime** | **Claude via the Anthropic SDK** (`anthropic` Python) | Judge model **Claude Sonnet 4.6** (`claude-sonnet-4-6`) by default for cost-effective rubric scoring; **Claude Opus 4.8** (`claude-opus-4-8`) escalation for ambiguous/borderline submissions. Cheap pre-filter classification on **Claude Haiku 4.5** (`claude-haiku-4-5`). Structured outputs (`output_config.format` / `messages.parse()`) make evaluation results schema-valid by construction. |
| **Frontend (learner + facilitator web)** | **TypeScript + React (Next.js)** | Standard SPA/SSR stack for the frontend dev + designer. Server components keep PF gating server-authoritative. |
| **Datastore** | **PostgreSQL 16** (+ JSONB), **Redis**, **S3-compatible object store** | See [[ADR-002-database]]. |
| **Job queue** | **Redis + RQ** (or Celery if scheduling complexity grows) | Evaluation is async; the API enqueues, the worker consumes. Redis already present for caching/sessions. |
| **Auth** | **OIDC (corporate SSO) + first-party email/password fallback**, JWT access tokens, org/cohort/role model | Corporate-first B2B: org admins enrol employees. See data model `Organization`/`Cohort`/`Membership`. |
| **Observability** | Structured JSON logging + OpenTelemetry traces; evaluation cost/usage captured per `EvaluationResult` | LLM spend is a first-class cost; track `usage` (input/output/cache tokens) on every judge call. |

### Model-selection policy (locked)

- **Default judge:** `claude-sonnet-4-6` — $3/$15 per MTok, 1M context, structured outputs + adaptive thinking.
- **Escalation judge:** `claude-opus-4-8` — used only when the Sonnet judge reports low confidence or two rubric passes disagree.
- **Pre-filter / cheap classification** (e.g. "is this a genuine attempt vs empty submission"): `claude-haiku-4-5`.
- **Batch grading** of non-latency-sensitive cohort submissions: Anthropic **Batches API** (50% cost) where turnaround within ~1h is acceptable.
- Use **adaptive thinking** (`thinking: {type: "adaptive"}`) with `effort` tuned per judge tier. Never hard-code `budget_tokens` (removed on 4.7+/4.8).

> Model IDs are exact strings — no date suffixes. Do not downgrade tiers for cost without a recorded decision; tier choice is a pedagogy/quality lever, not just a billing one.

## Consequences

**Positive**
- One backend language (Python) spans API, curriculum engine, and evaluator — small crew, shared domain models.
- FastAPI auto-generates an OpenAPI surface consistent with our hand-authored contract (`api/mahir-api.yaml`).
- Claude structured outputs make `EvaluationResult` valid-by-construction, removing a class of parsing bugs.
- Async evaluator decouples slow agent-run/judge latency from the request path.

**Negative / costs**
- Python evaluator running learner code demands a real sandbox (container-per-submission); this is operational work — see [[ADR-003-evaluator-design]].
- LLM-judge spend scales with submissions × rubric passes. Mitigated by tiering (Haiku→Sonnet→Opus), Batches, and prompt caching of the shared rubric prefix.
- Two languages total (Python + TypeScript) — acceptable, conventional split.

**Neutral**
- No Kubernetes for the pilot. Single VM / managed container host + managed Postgres is sufficient. Revisit at platform stage.
- Deploy contract (`DEFINITION.md`): staging-local-first, autodeploy OFF, branch pinned, smoke test before cutover — this stack must honour that gate.
