# Mahir — Async Evaluation Event Contract

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Related:** [[ADR-003-evaluator-design]], [[ADR-004-productive-failure-sequencing]], [[ADR-005-service-decomposition]], data-model.md, api/mahir-api.yaml

## Purpose

Evaluation is asynchronous (queue in, event/DB out). This contract defines the messages crossing the API ↔ Evaluator boundary. The transport for the pilot is **Redis** (RQ/Celery) per [[ADR-001-tech-stack]]; the **envelope and payloads here are transport-agnostic** so we can move to a managed broker later without changing producers/consumers.

## Envelope

Every message shares this envelope:

```jsonc
{
  "event_id": "uuidv7",          // unique per message; consumers dedupe on this
  "event_type": "evaluation.requested",
  "schema_version": "1.0",
  "occurred_at": "2026-06-11T00:00:00Z",
  "correlation_id": "uuidv7",    // = submission_id; ties the lifecycle together
  "producer": "api | evaluator",
  "data": { /* type-specific, below */ }
}
```

**Delivery semantics:** at-least-once. Consumers MUST be idempotent (dedupe on `event_id`; the terminal DB write is keyed by `submission_id` and is upsert-safe).

## Event types

### 1. `evaluation.requested`  (API → Evaluator)

Emitted when a learner POSTs a submission (`202`). Enqueues grading.

```jsonc
{
  "event_type": "evaluation.requested",
  "correlation_id": "<submission_id>",
  "data": {
    "submission_id": "uuidv7",
    "exercise_id": "uuidv7",
    "enrolment_id": "uuidv7",
    "attempt_number": 3,
    "payload_ref": { "kind": "inline|object_store",
                     "value": "…or s3 pointer + checksum…" },
    "rubric_snapshot_ref": "uuidv7",   // pinned exercise version for reproducibility
    "priority": "interactive|batch"     // batch → Batches API path (50% cost)
  }
}
```

> `rubric_snapshot_ref` pins the exact exercise/rubric/scenario version so a re-grade is reproducible even if content later changes.

### 2. `evaluation.started`  (Evaluator → system)  *(optional, observability)*

Marks `Submission.status = running`. Lets the UI show "evaluating…".

```jsonc
{
  "event_type": "evaluation.started",
  "correlation_id": "<submission_id>",
  "data": { "submission_id": "uuidv7", "worker_id": "…", "stage": "sandbox" }
}
```

### 3. `evaluation.completed`  (Evaluator → system)

The terminal success event. Carries the full structured `EvaluationResult` ([[ADR-003-evaluator-design]] / `EvaluationResult` schema in api/mahir-api.yaml). On receipt:
1. Persist the `EvaluationResult`, set `Submission.status = evaluated`.
2. **Recompute `ExerciseProgress`** per the [[ADR-004-productive-failure-sequencing]] gate (genuine-attempt accounting, variety, phase transition).

```jsonc
{
  "event_type": "evaluation.completed",
  "correlation_id": "<submission_id>",
  "data": {
    "submission_id": "uuidv7",
    "result": { /* full EvaluationResult — see api/mahir-api.yaml */ }
  }
}
```

### 4. `evaluation.failed`  (Evaluator → system)

Infrastructure failure (sandbox crashed, judge unrecoverable, timeout) — **distinct from a learner whose agent legitimately failed scenarios** (that is a *successful* `evaluation.completed` with `passed=false`).

```jsonc
{
  "event_type": "evaluation.failed",
  "correlation_id": "<submission_id>",
  "data": {
    "submission_id": "uuidv7",
    "reason": "sandbox_timeout|judge_error|internal",
    "retryable": true,
    "attempts": 2,
    "detail": "…"
  }
}
```

Sets `Submission.status = failed`. Retryable failures are re-enqueued with backoff up to a cap; non-retryable surface to the learner as "we couldn't grade this — resubmit" and to facilitators as an alert. A failed evaluation **never** advances the PF gate.

## State transitions driven by events

```
POST submission ──▶ status=queued ──evaluation.requested──▶ [Evaluator]
                                   ──evaluation.started──▶ status=running
   ┌─────────────────────────────────────────────────────────────┐
   │ evaluation.completed ─▶ status=evaluated ─▶ recompute         │
   │                         ExerciseProgress gate (ADR-004)       │
   │ evaluation.failed    ─▶ status=failed (retry or surface)      │
   └─────────────────────────────────────────────────────────────┘
```

## Invariants

1. **Idempotency:** processing the same `event_id` twice has no additional effect.
2. **Gate recompute is the only writer of phase transitions** on `evaluation.completed`; producers never set phase directly.
3. **Failure ≠ low score:** `evaluation.failed` is infrastructure; a low/failed grade is a normal `evaluation.completed`. The PF gate only ever consumes `completed` results.
4. **Reproducibility:** every grade references the pinned `rubric_snapshot_ref`, so re-grades are deterministic w.r.t. content version.
5. **Cost is carried through:** token `usage` + `cost_micro_usd` ride on the `EvaluationResult` inside `evaluation.completed` and are persisted for per-exercise/cohort spend reporting.
