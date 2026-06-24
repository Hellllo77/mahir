# ADR-003 — Evaluator Design

- **Status:** Accepted
- **Date:** 2026-06-11
- **Author:** atlas-architect-mahir
- **Task:** ARCH-001
- **Related:** [[ADR-001-tech-stack]], [[ADR-004-productive-failure-sequencing]], [[ADR-005-service-decomposition]], api/mahir-api.yaml, events/evaluation-events.md

## Context

The Evaluator grades **agent-build submissions** — learners build AI agents (prompts + config + small code), and the Evaluator must assess them. It is the hardest component because it has two jobs that pull in different directions:

1. **Assess agent quality** against an exercise rubric — does the built agent actually do X, robustly, across scenarios?
2. **Produce Productive-Failure signals** that the Curriculum Engine's gate ([[ADR-004-productive-failure-sequencing]]) consumes — distinguish *productive failure* (genuine, varied exploration) from *low-effort* or *off-task* submissions, **without** treating failure as bad.

A naive autograder (pass/fail) is wrong for Mahir: in PF, **early failure is the expected, valued path**, and the system must reward exploration, not just correctness.

Forces:
- Running learner-built agents means **executing untrusted code/prompts** → isolation is mandatory.
- Grading agent *quality* (not just exact output) needs judgment → an **LLM-judge** using Claude.
- Judge calls cost money and scale with submissions × passes → cost tiering matters.
- Results feed a gate → results must be **schema-valid and structured**, not free text.

## Decision

A **two-stage evaluator**: a **deterministic scenario harness** (runs the agent in a sandbox against fixed scenarios) followed by an **LLM-judge** (scores quality + emits PF signals), composed in the async Evaluator worker tier from [[ADR-005-service-decomposition]].

```
submission ─▶ ┌──────────────┐   transcripts/   ┌───────────────────┐
              │ Stage 1:      │   outputs        │ Stage 2:           │
              │ Sandbox runner│ ───────────────▶ │ LLM-judge (Claude) │
              │ (container    │                  │ rubric scoring +   │
              │  per submission│                 │ PF-signal + approach│
              │  scenario      │                  │ detection          │
              │  harness)      │                  └─────────┬─────────┘
              └──────────────┘                              │
                  deterministic checks                       ▼
                  (does it run? schema? tool-calls?)    EvaluationResult
                                                        (structured, schema-valid)
```

### Stage 1 — Deterministic scenario harness (in sandbox)

- Each exercise defines **scenarios** (fixed inputs + expected-behaviour assertions) and **deterministic checks** (does the agent load/run? valid config? required tool declared? no banned calls?).
- The learner's built agent runs **inside an isolated sandbox** against each scenario. Captured: transcripts, tool calls, outputs, errors, runtime.
- **Isolation:** container-per-submission, no inbound network, egress restricted to the LLM endpoint only, CPU/mem/time limits. (When/if we adopt Anthropic **Managed Agents** to host learner-agent execution, use a `self_hosted` or networking-`limited` environment so the blast radius stays ours — see *Sandboxing* below.)
- Stage 1 alone yields hard signals: ran/didn't, passed/failed each scenario assertion, banned-pattern hits.

### Stage 2 — LLM-judge (Claude)

The judge reads the rubric + the Stage-1 transcripts/outputs and produces a **structured** `EvaluationResult` — never free text. Locked design:

- **Structured outputs.** The judge call uses `output_config.format` with a JSON Schema (the `EvaluationResult` schema), or `client.messages.parse()` with a Pydantic model. The result is **valid-by-construction**; no fragile parsing.
- **Rubric criteria scored independently.** Each rubric criterion is graded with its own `score`, `evidence` (must cite a Stage-1 transcript/output — no ungrounded claims), and `met` boolean. "Report coverage, filter later" — the judge surfaces all criteria with confidence + severity; the gate decides.
- **PF signal is a first-class output.** The judge classifies `productive_failure_signal ∈ {productive, low_effort, off_task}` and a `detected_approach` taxonomy code, with `confidence`. These feed [[ADR-004-productive-failure-sequencing]]'s gate directly. The prompt explicitly instructs: *failure is expected; reward genuine, varied exploration; penalise only empty/copied/off-task work.*
- **Model tiering** (per [[ADR-001-tech-stack]]):
  - Cheap pre-filter on **`claude-haiku-4-5`**: is this a genuine attempt at all? Short-circuits empty/junk before paying for a full judge.
  - Default judge on **`claude-sonnet-4-6`** with **adaptive thinking** + tuned `effort`.
  - Escalate to **`claude-opus-4-8`** only when Sonnet reports low confidence or two rubric passes disagree (adversarial second opinion).
  - **Batch grading** of non-urgent cohort runs via the **Batches API** (50% cost) where ~1h turnaround is acceptable.
- **Prompt caching.** The rubric + scenario context is a large, stable prefix shared across all submissions for an exercise → cache it (`cache_control: ephemeral`) so per-submission cost is only the varying transcript. Keep volatile per-submission content *after* the cached prefix.
- **Cost accounting.** Every judge call records `usage` (input / output / cache-read tokens), model ID, and an estimated cost onto the `EvaluationResult` (per [[ADR-002-database]]). LLM spend is queryable per exercise/cohort.

### The `EvaluationResult` (shape summary; canonical in data-model.md)

```jsonc
{
  "schema_version": "1.0",
  "submission_id": "…",
  "status": "evaluated",
  "ran": true,
  "scenario_results": [ { "scenario_id": "…", "passed": true, "detail": "…" } ],
  "rubric_scores": [
    { "criterion_id": "…", "met": false, "score": 0.4,
      "confidence": 0.8, "severity": "major",
      "evidence": "transcript#scenario-2: agent never called the search tool" }
  ],
  "overall_score": 0.55,
  "productive_failure_signal": "productive",   // productive | low_effort | off_task
  "detected_approach": "approach.single-prompt-no-tools",
  "confidence": 0.82,
  "passed": false,                              // failing is fine — see ADR-004
  "feedback_markdown": "…learner-facing, PF-aware feedback…",
  "judge": { "model": "claude-sonnet-4-6", "escalated": false,
             "usage": { "input_tokens": 0, "output_tokens": 0,
                        "cache_read_input_tokens": 0 } }
}
```

### Sandboxing (decision)

- **Pilot:** container-per-submission on the Evaluator tier, network egress allow-listed to the Anthropic API only, hard CPU/mem/wall-clock limits, no persistent state between submissions.
- **If/when learner agents need a fuller runtime,** prefer Anthropic **Managed Agents** with a `self_hosted` environment (tool execution on our infra) **or** a `cloud` environment with `limited` networking — never `unrestricted`. Secrets (our API key) **never enter the sandbox**: route the agent's model calls through a host-side proxy/custom-tool so a learner submission cannot exfiltrate credentials.

## Consequences

**Positive**
- Structured outputs make results gate-ready and parse-safe.
- Two-stage design separates *did it run / pass scenarios* (cheap, deterministic) from *how good / how exploratory* (LLM judgment) — each is independently tunable.
- PF signals are produced where the evidence lives (the judge sees the transcripts), keeping [[ADR-004-productive-failure-sequencing]]'s gate honest.
- Tiering + caching + Batches keep LLM spend bounded and *measured*.

**Negative**
- Running untrusted learner agents is the platform's sharpest security edge; sandboxing is real, ongoing operational work and a standing review item.
- LLM-judge introduces non-determinism in scores; mitigated by grounded `evidence` requirements, independent criteria, confidence reporting, and Opus escalation on disagreement. Judges are advisory to facilitators, not infallible.
- Judge cost grows with cohort size; Batches + Haiku pre-filter + cached rubric prefix are the levers, and cost is tracked per result to catch drift.

**Neutral**
- The evaluator is asynchronous (queue in, event/DB out). The UI reflects `submission.status` transitions; instant grading is neither required nor pedagogically desirable.
- The PF taxonomy (`detected_approach` codes) is exercise-authored configuration, co-evolving with [[ADR-004-productive-failure-sequencing]] thresholds.
