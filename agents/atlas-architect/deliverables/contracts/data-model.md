# Mahir — Canonical Data Model

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Scope:** Co-Worker (corporate) pilot
- **Authority:** This is the canonical data model. Specialist work (backend, QA) builds against this. Changes are immutable once accepted — propose amendments via RFC.
- **Related:** [[ADR-002-database]], [[ADR-004-productive-failure-sequencing]], [[ADR-003-evaluator-design]], api/mahir-api.yaml

## Conventions (from [[ADR-002-database]])

- **PKs:** `UUIDv7` (time-sortable), column `id`.
- **Audit:** every top-level entity has `created_at`, `updated_at` (timestamptz), `deleted_at` (nullable, soft delete), and `created_by` / `updated_by` (actor user id, nullable for system).
- **JSONB payloads** carry a `schema_version` string; validated by Pydantic at the API boundary.
- **Money/cost:** integers in micro-USD (`cost_micro_usd`) to avoid float drift.
- Naming: snake_case tables/columns; FK columns `<entity>_id`.

## Domain map

```
Organization 1───* Cohort 1───* Enrolment *───1 User
     │                  │                          │
     │                  └── facilitated_by ─────── User (facilitator)
     │
Curriculum (versioned)
  Module 1───* Exercise 1───* Scenario
                   │     └──* RubricCriterion
                   │     └──* ApproachTaxonomy (PF approach codes)
                   │     └── ConsolidationContent (1:1, gated)
                   │
ExerciseProgress *───1 User, *───1 Exercise   (PF phase state — server-authoritative)
        │
        1───* Submission 1───1 EvaluationResult
```

---

## 1. Identity & Org (Auth module)

### Organization
Corporate customer (grant-funded pilot tenant).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| name | text | |
| slug | text | unique |
| edition | enum(`co_worker`,`co_founder`) | pilot = `co_worker` |
| region | text | data-residency tag (e.g. `my`, `sg`) |
| sso_config | jsonb (nullable) | OIDC issuer/client metadata; `schema_version` |
| status | enum(`active`,`suspended`) | |
| + audit | | |

### User
A person. Belongs to one Organization (pilot scope: single-org membership).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| organization_id | uuidv7 | FK → Organization |
| email | citext | unique within org |
| display_name | text | |
| auth_provider | enum(`oidc`,`local`) | |
| external_subject | text (nullable) | OIDC `sub` |
| password_hash | text (nullable) | local fallback only |
| global_role | enum(`learner`,`facilitator`,`org_admin`,`super_admin`) | coarse role; fine-grained per-cohort via Enrolment |
| status | enum(`invited`,`active`,`deactivated`) | |
| + audit | | |

### Cohort
A training group within an org (e.g. "KrakenCorp Q3 2026 intake").

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| organization_id | uuidv7 | FK → Organization |
| name | text | |
| curriculum_id | uuidv7 | FK → Curriculum (pinned version the cohort runs) |
| starts_on / ends_on | date (nullable) | |
| status | enum(`draft`,`running`,`completed`,`archived`) | |
| + audit | | |

### Enrolment
Membership of a User in a Cohort, with per-cohort role.

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| cohort_id | uuidv7 | FK → Cohort |
| user_id | uuidv7 | FK → User |
| role | enum(`learner`,`facilitator`) | |
| status | enum(`active`,`withdrawn`,`completed`) | |
| + audit | | unique(cohort_id, user_id) |

---

## 2. Curriculum (Curriculum Engine module)

### Curriculum
A versioned curriculum container. Cohorts pin a specific version (immutability for in-flight cohorts).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| edition | enum(`co_worker`,`co_founder`) | |
| title | text | |
| version | text | semver; immutable once `published` |
| status | enum(`draft`,`published`,`archived`) | |
| + audit | | |

### Module
Ordered unit within a Curriculum.

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| curriculum_id | uuidv7 | FK → Curriculum |
| title | text | |
| sequence_index | int | order within curriculum |
| summary_markdown | text | |
| + audit | | |

### Exercise
The PF unit: a complex problem the learner attempts by building an agent. Carries the PF gate hyperparameters ([[ADR-004-productive-failure-sequencing]]).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| module_id | uuidv7 | FK → Module |
| title | text | |
| sequence_index | int | order within module |
| prompt_markdown | text | the ill-structured problem statement (no canonical method) |
| build_spec | jsonb | what the learner must build (agent type, allowed tools, IO contract); `schema_version` |
| prerequisite_exercise_ids | uuidv7[] | must be COMPLETED before start |
| **min_attempts** | int default 2 | PF gate: genuine attempts required |
| **min_distinct_approaches** | int default 2 | PF gate: representational variety |
| **min_exploration_seconds** | int default 300 | PF gate: depth/time floor |
| allow_fast_unlock | bool default true | escape hatch for outright pass on attempt 1 |
| + audit | | |

### Scenario
A fixed test case the learner's agent is run against (Stage 1 of [[ADR-003-evaluator-design]]).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| exercise_id | uuidv7 | FK → Exercise |
| name | text | |
| input_payload | jsonb | scenario input given to the agent; `schema_version` |
| assertions | jsonb | deterministic expected-behaviour checks; `schema_version` |
| weight | numeric | contribution to scenario score |
| + audit | | |

### RubricCriterion
A single, independently-graded quality dimension (Stage 2 judge scores each).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| exercise_id | uuidv7 | FK → Exercise |
| code | text | stable criterion id |
| description | text | what "met" means |
| weight | numeric | |
| guidance_markdown | text | judge instructions for this criterion |
| + audit | | |

### ApproachTaxonomy
The set of recognised solution approaches for an exercise; the judge tags submissions with one of these `code`s, feeding the variety gate.

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| exercise_id | uuidv7 | FK → Exercise |
| code | text | e.g. `approach.single-prompt-no-tools` |
| label | text | |
| is_canonical | bool | marks the intended/expert approach |
| + audit | | |

### ConsolidationContent
The canonical solution + teardown, revealed only after the PF gate passes (1:1 with Exercise).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| exercise_id | uuidv7 | FK → Exercise, unique |
| body_markdown | text | reference design + why it works |
| reference_build | jsonb | the canonical agent build; `schema_version` |
| check_questions | jsonb (nullable) | consolidation comprehension check |
| + audit | | |

---

## 3. Progress (Progress Store module)

### ExerciseProgress
**Server-authoritative PF phase state** per (learner, exercise). Single source of truth for what content a learner may see ([[ADR-004-productive-failure-sequencing]]).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| enrolment_id | uuidv7 | FK → Enrolment (binds learner+cohort) |
| exercise_id | uuidv7 | FK → Exercise |
| **phase** | enum(`not_started`,`exploring`,`consolidation_unlocked`,`completed`) | the state machine |
| attempts_total | int | all submissions |
| attempts_genuine | int | productive/passed submissions counting toward gate |
| distinct_approaches | int | count of distinct detected approach codes seen |
| exploration_seconds | int | accumulated time in `exploring` |
| explored | bool | false if unlocked via fast-unlock escape hatch |
| unlocked_at | timestamptz (nullable) | when consolidation unlocked |
| completed_at | timestamptz (nullable) | |
| mastery_score | numeric (nullable) | best/aggregate overall_score |
| facilitator_override | jsonb (nullable) | audited manual gate override |
| + audit | | unique(enrolment_id, exercise_id) |

---

## 4. Submissions & Evaluation (Evaluator)

### Submission
One agent-build attempt by a learner at an exercise.

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| exercise_progress_id | uuidv7 | FK → ExerciseProgress |
| enrolment_id | uuidv7 | FK → Enrolment (denormalised for query) |
| exercise_id | uuidv7 | FK → Exercise (denormalised) |
| attempt_number | int | 1-based within the (learner,exercise) |
| **payload** | jsonb | the agent build: prompt(s), config, inline code; `schema_version` |
| artifact_refs | jsonb (nullable) | object-store pointers + checksums for larger bundles |
| **status** | enum(`queued`,`running`,`evaluated`,`failed`) | async lifecycle |
| idempotency_key | text | unique; dedupes double-submits |
| submitted_at | timestamptz | |
| + audit | | |

### EvaluationResult
Structured grading output (1:1 with Submission). Schema is valid-by-construction via Claude structured outputs ([[ADR-003-evaluator-design]]).

| Column | Type | Notes |
|--------|------|-------|
| id | uuidv7 | PK |
| submission_id | uuidv7 | FK → Submission, unique |
| schema_version | text | |
| ran | bool | did the agent execute at all (Stage 1) |
| scenario_results | jsonb | `[{scenario_id, passed, detail}]` |
| rubric_scores | jsonb | `[{criterion_id, met, score, confidence, severity, evidence}]` — evidence must cite a transcript |
| overall_score | numeric | 0..1 |
| **productive_failure_signal** | enum(`productive`,`low_effort`,`off_task`) | feeds PF gate |
| **detected_approach** | text | FK-by-code → ApproachTaxonomy.code |
| confidence | numeric | judge confidence 0..1 |
| passed | bool | failing is fine (PF) |
| feedback_markdown | text | learner-facing, PF-aware feedback |
| feedback_artifact_ref | jsonb (nullable) | object-store pointer if rich (DOCX/PDF) feedback generated |
| judge_model | text | e.g. `claude-sonnet-4-6` |
| judge_escalated | bool | true if Opus 4.8 second opinion used |
| usage_input_tokens / usage_output_tokens / usage_cache_read_tokens | int | cost accounting |
| cost_micro_usd | int | estimated judge spend |
| evaluated_at | timestamptz | |
| + audit | | |

---

## Lifecycle invariants (must hold)

1. **Phase gating:** `ConsolidationContent` and `GET /exercises/{id}/consolidation` are served **only** when `ExerciseProgress.phase ∈ {consolidation_unlocked, completed}`. Enforced server-side.
2. **Genuine-attempt accounting:** `attempts_genuine` increments only when an `EvaluationResult` has `productive_failure_signal = productive` **or** `passed = true`. `low_effort`/`off_task` never count toward the gate.
3. **Variety:** `distinct_approaches` = count of distinct `detected_approach` codes across the learner's genuine submissions for that exercise.
4. **Async consistency:** a `Submission` is `queued → running → evaluated|failed`; `ExerciseProgress` is recomputed on `evaluation.completed` (see events/evaluation-events.md), never synchronously at submit time.
5. **Versioned content immutability:** a `published` Curriculum version is immutable; running cohorts pin a version so content cannot shift under in-flight learners.
6. **Audit everywhere:** every gate transition, facilitator override, and judge escalation is recorded (corporate/grant auditability).
