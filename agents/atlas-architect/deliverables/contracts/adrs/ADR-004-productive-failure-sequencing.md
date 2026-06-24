# ADR-004 — Productive Failure Sequencing Logic

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Related:** [[ADR-003-evaluator-design]], [[ADR-005-service-decomposition]], data-model.md, api/mahir-api.yaml

## Context

Productive Failure (Kapur) is Mahir's pedagogical core, not a feature. The method **inverts** conventional instruction:

1. **Generation / Exploration phase** — the learner is given a complex, ill-structured problem **before being taught the canonical method**. They generate multiple representations and solution attempts (RSMs). Most attempts are *expected to fail*. This generation primes the learner.
2. **Consolidation / Instruction phase** — only *after* genuine exploration is the canonical solution revealed. The learner compares their attempts to it; the prior failure makes the consolidation "stick."

For an agent-building curriculum, the "problem" is *build an agent that does X*, attempts are **agent-build submissions** evaluated by [[ADR-003-evaluator-design]], and consolidation is the reference design + teardown.

The architectural requirement: **the engine must enforce the PF sequence server-side**. Consolidation content must be *gated* behind sufficient, genuine exploration — and "genuine" must be measured, because PF fails if learners either (a) get the answer too early or (b) disengage and submit junk.

## Decision

Model each exercise as a **server-authoritative phase state machine** owned by the Curriculum Engine, with transitions driven by exploration signals from the Evaluator.

### Phases

```
            ┌─────────────┐
            │  NOT_STARTED │
            └──────┬───────┘
                   │ learner opens exercise
                   ▼
            ┌─────────────┐   submit attempt(s)      ┌──────────────────┐
            │  EXPLORING   │ ───────────────────────▶ │ (attempts graded  │
            │ (generation) │ ◀─────────────────────── │  by Evaluator)    │
            └──────┬───────┘   result + PF signals    └──────────────────┘
                   │ exploration-sufficiency gate satisfied
                   ▼
            ┌──────────────────────┐
            │ CONSOLIDATION_UNLOCKED│  reference design + teardown revealed
            └──────────┬───────────┘
                       │ learner completes consolidation check
                       ▼
                 ┌───────────┐
                 │ COMPLETED  │
                 └───────────┘
```

Consolidation content is **never** served while phase ∈ {`NOT_STARTED`, `EXPLORING`}. The API for consolidation (`GET /exercises/{id}/consolidation`) returns `409 phase_locked` until the gate passes. This is enforced in the Curriculum Engine, not the client.

### The exploration-sufficiency gate

Transition `EXPLORING → CONSOLIDATION_UNLOCKED` requires **all** of:

1. **Minimum genuine attempts** — `attempts_genuine >= exercise.min_attempts` (default 2). "Genuine" is asserted by the Evaluator's **productive-failure signal**, not by pass/fail. A submission that is empty, trivially copied, or a known anti-pattern does **not** count toward the minimum.
2. **Representational variety** — the learner's attempts span `>= exercise.min_distinct_approaches` distinct detected approaches (default 2). The Evaluator tags each submission with a detected `approach` taxonomy code; the gate counts distinct codes. This operationalises PF's "generate diverse RSMs."
3. **Exploration depth/time floor** — `time_in_exploration >= exercise.min_exploration_seconds` (a low floor, default ~5 min) to prevent gaming by rapid junk submissions.

A **fast-unlock escape hatch**: if a learner *passes* the exercise outright on attempt 1 with high confidence, they may still be offered consolidation — but flagged `explored=false` so facilitators see PF was bypassed (a strong learner is not forced to fail artificially; the pedagogy is logged, not coerced).

> Crucially: **passing is not the gate, and failing is not penalised.** The gate measures *productive exploration*. This is what distinguishes Mahir's engine from an autograder.

### Inputs to the gate (from the Evaluator)

Each `EvaluationResult` supplies, per [[ADR-003-evaluator-design]]:
- `productive_failure_signal` ∈ {`productive`, `low_effort`, `off_task`} — only `productive` (and `passed`) attempts count toward `attempts_genuine`.
- `detected_approach` — taxonomy code feeding the variety check.
- `confidence` — used for the fast-unlock escape hatch.

### Module-level sequencing

Exercises within a module are ordered (`sequence_index`). A module's later exercises may declare `prerequisite_exercise_ids`; the engine refuses to start an exercise whose prerequisites are not `COMPLETED`. Cohort facilitators may override gates per learner (recorded, audited).

## Consequences

**Positive**
- The pedagogy is **enforced and observable**: gating lives in one server-side state machine, every transition is auditable, and facilitators get real signals (explored vs bypassed, variety, effort).
- Decoupling the *gate decision* (Curriculum Engine) from the *signal production* (Evaluator) lets us tune pedagogy thresholds without touching grading, and vice-versa.
- "Failing is fine, exploring is required" is encoded structurally, protecting the method from autograder-creep.

**Negative**
- The gate depends on Evaluator signals being trustworthy; a weak `productive_failure_signal` weakens the pedagogy. This raises the bar on [[ADR-003-evaluator-design]] — the signal is a first-class evaluator output, not an afterthought.
- Thresholds (`min_attempts`, `min_distinct_approaches`, `min_exploration_seconds`) are pedagogical hyperparameters that need pilot tuning. They are therefore **per-exercise configuration**, not hard-coded constants.

**Neutral**
- Phase state is per `(learner, exercise)` and stored in the Progress Store. It is the single source of truth for what content a learner may see.
- The escape hatch means PF is the *default*, not a cage — consistent with adult corporate learners.
