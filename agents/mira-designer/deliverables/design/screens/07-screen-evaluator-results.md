# Screen Spec: Evaluator Results
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Route:** `/exercises/[exerciseId]/results/[submissionId]` · also inline in challenge interface  
**Role:** Learner (primary) · Facilitator (read-only access)

---

## Purpose

Full evaluation result view for a single submission. The learner understands why they scored what they scored, what PF signal was detected, and what to improve. The view must be honest about the `low_effort`/`off_task` signals without being demotivating, and must surface quality evidence at a level that enables improvement.

---

## Wireframe

```
┌────────────────────────────────────────────────────────────────────────┐
│ TopBar: [≡] Mahir  /  Module 2  /  Exercise 3  /  Attempt 2   Ahmad ▾ │
├─────────┬──────────────────────────────────────────────────────────────┤
│ Sidebar │                                                              │
│         │  Evaluation Result — Attempt 2                              │
│         │  Multi-Step Support Agent · Module 2 · Exercise 3           │
│         │                                                              │
│         │  ┌───────────────────────────────────────────────────────┐  │
│         │  │  ●78%         [Productive] ↑    Single-prompt         │  │
│         │  │   Overall     PF Signal        Detected approach       │  │
│         │  │                                                        │  │
│         │  │  ✓ Agent ran  ·  3/4 scenarios passed                 │  │
│         │  │  Evaluated by claude-sonnet-4-6 · 2026-06-11 14:32    │  │
│         │  └───────────────────────────────────────────────────────┘  │
│         │                                                              │
│         │  ── Scenarios  ──────────────────────────────────────────   │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✓  Basic escalation routing                            │ │
│         │  │    Agent correctly identified escalation trigger       │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✓  Context collection                                  │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✓  Multi-language input                                │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✗  Edge case: empty payload            [Details ▼]     │ │
│         │  │    The agent threw an unhandled error on empty input   │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ── Rubric  ─────────────────────────────────────────────   │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✓  Prompt clarity           ████████░░   0.8 / 1.0    │ │
│         │  │    Evidence: "System prompt clearly states escalation  │ │
│         │  │    rules and output format."                           │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ✓  Error handling           ████████████  1.0 / 1.0   │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ ⚠  Edge case coverage       ████░░░░░░░░  0.4 / 1.0   │ │
│         │  │    Evidence: "No handling observed for empty/null      │ │
│         │  │    input payloads. Assertion on scenario 4 failed."    │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ── Feedback  ───────────────────────────────────────────   │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ Your escalation logic is solid and the context         │ │
│         │  │ collection works well across most scenarios. The main  │ │
│         │  │ gap is input validation — the agent fails entirely on  │ │
│         │  │ empty payloads. Try wrapping your input processing in  │ │
│         │  │ a validation step before the main logic runs.          │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  [← Back to Exercise]  [Try Again →]  [Next Exercise →]    │
│         │                                                              │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## Component breakdown

| Region | Component | Notes |
|--------|-----------|-------|
| Result header card | Custom summary card | Score, PF signal, approach, metadata |
| Scenario section | `ScenarioResultRow` × N | Collapsible detail |
| Rubric section | `RubricScoreRow` × N | Inline mini progress bar + evidence |
| Feedback section | Rendered markdown | `feedback_markdown` from `EvaluationResult` |
| Actions | `Button` × 3 | Back, Try Again, Next Exercise |

---

## Result header card spec

```
┌───────────────────────────────────────────────────────┐
│  [score]        [PF signal badge]  [Approach]         │
│  Overall        PF Signal          Detected approach  │
│                                                        │
│  [✓ / ✗] Agent ran   [n]/[total] scenarios passed    │
│  Evaluated by [judge_model]   [evaluated_at]           │
└───────────────────────────────────────────────────────┘
```

**Score display:**
- Value: `--text-3xl`, `--weight-bold`, `tabular-nums`
- Color by score: <50% = `--color-error-700`, 50–79% = `--color-warning-700`, ≥80% = `--color-success-700`
- Background: white card, `--shadow-sm`, `--radius-lg`
- Padding: `--space-6`

**PF signal badge:** `PFSignalBadge` component (see #19). Displayed prominently — this is not a secondary label.

**Detected approach:** `--text-sm`, `--color-neutral-600`. Shows `ApproachTaxonomy.label`. If `is_canonical = true`, append "(canonical approach)" in success-700.

**Agent ran:** `CheckCircle2` success if `ran = true`; `XCircle` error if `ran = false`. If `ran = false`, short alert: "Your agent did not execute. Check for syntax errors in your build."

**Evaluator metadata:** `--text-xs`, `--color-neutral-500`. Right-aligned or below the main row. "Evaluated by [judge_model]" + if `judge_escalated = true`: "+ Opus 4.8 second opinion" badge. Cost not shown to learner.

---

## Scenarios section

Heading: "Scenarios" + badge `[n/total passed]` (success if all passed, warning otherwise).

Each `ScenarioResultRow`:
```
┌──────────────────────────────────────────────────────┐
│ [✓|✗]  [Scenario name]                  [Details ▼] │
│         [detail text — collapsed by default]         │
└──────────────────────────────────────────────────────┘
```

- Passed: `CheckCircle2` `--color-success-500`, left border 3px `--color-success-500`
- Failed: `XCircle` `--color-error-500`, left border 3px `--color-error-500`
- Detail: `<details>` collapsible; `--font-mono`, `--text-mono-sm`, `--color-neutral-700`
- Expand all / Collapse all toggle: small ghost button top-right of section

---

## Rubric section

Heading: "Rubric" + `--text-sm` subheading: "Quality assessment across [n] criteria"

Each `RubricScoreRow`:
```
┌──────────────────────────────────────────────────────┐
│ [✓|⚠]  [Criterion label]   [bar]  [score] / 1.0    │
│         Confidence: [n]%                             │
│         Evidence: "[verbatim text from result]"      │
└──────────────────────────────────────────────────────┘
```

**Score bar:** Inline progress bar 120px wide × 6px tall. Fill color:
- ≥0.8 = `--color-success-500`
- 0.5–0.79 = `--color-warning-500`
- <0.5 = `--color-error-500`

**Met icon:**
- `met = true` + score ≥0.8: `CheckCircle2` success-500
- `met = true` + score <0.8: `CheckCircle2` warning-500 (partially met)
- `met = false`: `AlertTriangle` error-500

**Confidence:** Small `--text-xs` `--color-neutral-500` below criterion label. E.g. "Confidence: 92%". Only shown if `confidence < 0.75` (high confidence is noise; low confidence is signal to learner).

**Evidence:** Verbatim quote from judge, `--font-mono`, `--text-xs`, `--color-neutral-600`. Background `--color-neutral-100`, radius `--radius-sm`, padding `--space-2`. Required field per data model — if absent show "No evidence provided" in neutral-400.

**Severity:** If `severity` is non-null (e.g. "critical", "minor"), show as small badge: `--color-error-100` for critical, `--color-warning-100` for minor.

---

## Feedback section

Heading: "Feedback"

Rendered `feedback_markdown` via `react-markdown`. Constrained to prose width (max 640px within the section). `--text-base`, `--leading-relaxed`.

**Tone guard:** The feedback text comes from the LLM judge — wren-frontend should not modify it. The design around it (heading, spacing) should be neutral, not alarming.

**If `judge_escalated = true`:** Small info badge above feedback: "Reviewed by Opus 4.8 for this evaluation" — signals quality without confusing the learner.

---

## Actions bar

Bottom of page, sticky on scroll (`position: sticky; bottom: 0`):
```
[← Back to Exercise]      [Try Again →]       [Next Exercise →]
```

| Button | Condition | Action |
|--------|-----------|--------|
| `← Back to Exercise` | Always | Navigate to `/exercises/[id]/challenge` |
| `Try Again →` | `phase ≠ completed` | Navigate to challenge, BuildEditor pre-filled with this submission's payload |
| `Next Exercise →` | `phase = completed` OR next exercise unlocked | Navigate to next exercise in module |

"Try Again" behavior: the challenge page receives a query param `?copyFrom=[submissionId]` and pre-fills `BuildEditor` with the prior submission's payload. This saves the learner time while encouraging iteration.

---

## Submission history sidebar (full results page only)

On the full `/results/[submissionId]` route (not the inline panel in challenge), show a right-side drawer (280px) listing all submissions for this exercise:

```
Attempts (3)
─────────────────
▶ #3  78%  [Productive]   · 14:32
  #2  63%  [Productive]   · 14:10
  #1  48%  [Low Effort]   · 13:55
```

Selected attempt highlighted `--color-primary-50`. Click navigates to that submission's result URL (no full reload — SWR re-fetch).

---

## Low-effort / off-task feedback treatment

When `productive_failure_signal ∈ {low_effort, off_task}`:

- `PFSignalBadge` displayed normally (warning / error color)
- Score display not shown (or shown as "—") — overall score is not meaningful for off-task submissions
- Feedback markdown is shown
- Scenarios and rubric are shown in collapsed state by default with a note: "Detailed results are available, but focus on the feedback above."
- No "Try Again" pre-fill for low_effort (learner should start fresh)
- Copy in feedback section heading: "What to focus on" (not "Feedback" which sounds like a grade)

---

## States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| Loading | Route mounted | Skeleton for header card + 3 scenario rows + 3 rubric rows |
| Evaluated — productive | `signal = productive` | Full results shown |
| Evaluated — low_effort | `signal = low_effort` | Simplified view, focus-on-feedback treatment |
| Evaluated — off_task | `signal = off_task` | Simplified view, error alert at top |
| Agent didn't run | `ran = false` | Error callout at top; scenarios shown as N/A |
| Judge escalated | `judge_escalated = true` | Info badge in feedback section |

---

## Accessibility notes

- Page `<h1>` = "Evaluation Result — Attempt [n]"
- Score: `<data value="78">78%</data>` for machine-readable score
- PF signal: `role="status"` + `aria-label="Productive Failure signal: [signal]"`
- Scenario list: `<ul>` with `<li>` per row; expand/collapse: `<details>/<summary>`
- Rubric: `<ul>` with `<li>` per criterion; score bar: `<meter value="0.8" min="0" max="1" aria-label="[criterion]: 0.8 out of 1.0">`
- Evidence block: `<blockquote>` element
- Actions bar: `role="navigation" aria-label="Result actions"`
