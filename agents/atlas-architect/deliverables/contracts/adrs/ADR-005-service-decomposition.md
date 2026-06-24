# ADR-005 — Service Decomposition & Architecture Style

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Related:** [[ADR-001-tech-stack]], [[ADR-003-evaluator-design]], [[ADR-004-productive-failure-sequencing]]

## Context

The PRD names four components: **curriculum engine**, **evaluator service**, **learner-progress store**, and **auth layer**. We must decide how these are deployed and bounded for the **Co-Worker pilot**. The dominant forces:

- **Asymmetric runtime profile.** The curriculum/progress/auth paths are fast request/response (ms). The **evaluator is slow, bursty, and resource-heavy** (spawns sandboxes, calls LLMs over seconds-to-minutes).
- **Different blast radius.** Running learner-submitted agent code is the one place with real isolation/security requirements; everything else is ordinary CRUD + gating logic.
- **Small crew, pilot scale.** A full microservice mesh would be over-engineering. But coupling slow agent execution into the API process would starve request threads.

## Decision

Adopt a **modular monolith + a separate evaluator worker tier** — two deployable units, not a microservice fleet:

```
┌──────────────────────────────────────────────┐
│  Mahir API (modular monolith, FastAPI)         │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│  │ Auth       │ │ Curriculum │ │ Progress   │  │
│  │ module     │ │ Engine     │ │ Store      │  │
│  │ (OIDC/JWT) │ │ (PF state  │ │ (mastery,  │  │
│  │            │ │  machine)  │ │  attempts) │  │
│  └────────────┘ └─────┬──────┘ └────────────┘  │
│         shared domain models + Postgres access  │
└───────────────────────────┬────────────────────┘
                 enqueue eval │ (Redis queue)
                              ▼
              ┌───────────────────────────────┐
              │  Evaluator Worker tier (Python)│
              │  ┌─────────┐  ┌─────────────┐  │
              │  │ Sandbox │  │ Rubric +    │  │
              │  │ runner  │→ │ LLM-judge   │  │
              │  │(container│  │ (Claude)    │  │
              │  │ per sub) │  └─────────────┘  │
              │  └─────────┘                    │
              └──────────────┬─────────────────┘
                 writes result│ (Postgres + events)
                              ▼
                     Progress Store updated,
                     PF phase re-evaluated
```

- **Module boundaries are enforced in-code** (separate packages, no cross-module DB writes except via published domain services), so the modules *can* be split into services later without a rewrite.
- **Auth, Curriculum Engine, Progress Store** are modules of the one API deployable. They share one Postgres instance but own distinct schemas/tables (see `data-model.md`).
- **Evaluator** is a **separate process/tier** consuming a Redis queue. It is the only component that executes untrusted code and the only one that may scale independently (more workers under cohort-submission bursts).
- **Communication:** API → Evaluator is **asynchronous via queue** (`evaluation.requested`). Evaluator → system is **event + DB write** (`evaluation.completed`). See `events/evaluation-events.md`.

## Consequences

**Positive**
- Slow/heavy/untrusted evaluation work is isolated from the request path and from the rest of the data plane.
- One transaction boundary (one Postgres) for curriculum/progress/auth keeps PF gating consistent and simple — no distributed-transaction problem for the core learning loop.
- Modular packaging preserves a clean split-to-services path at platform stage without committing to the operational cost now.

**Negative**
- A shared database across modules requires discipline (schema ownership, no reach-across writes) to avoid a big-ball-of-mud. Enforced by review against this ADR and `data-model.md`.
- Two deployables to operate (API + worker) instead of one. Justified by the runtime asymmetry.

**Neutral**
- The async boundary means evaluation results are **eventually consistent** — the UI must reflect `submission.status` (`queued → running → evaluated`) rather than expecting synchronous grades. This is *also* pedagogically correct for PF (grading is reflective, not instant gating).
