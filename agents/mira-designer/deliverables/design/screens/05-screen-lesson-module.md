# Screen Spec: Lesson / Module View
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Route:** `/modules/[moduleId]`  
**Role:** Learner

---

## Purpose

Shows the module outline, all exercises in sequence, each with its current PF phase and gate status. Learner sees what they've done and what's next. Entry point to the challenge interface.

---

## Wireframe

```
┌────────────────────────────────────────────────────────────────────────┐
│ TopBar: [≡] Mahir  /  Modules  /  Module 2                 Ahmad · ▾ │
├─────────┬──────────────────────────────────────────────────────────────┤
│ Sidebar │                                                              │
│         │  Module 2                                                    │
│   Mods● │  Tool Use & Orchestration                                   │
│         │  4 exercises · 2 of 4 complete                              │
│         │                                                              │
│         │  Progress  ████████░░░░░░░░░░  2/4  50%                    │
│         │                                                              │
│         │  ── Exercises ───────────────────────────────────────────   │
│         │                                                              │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ 1  Ticket Classifier                    [Completed ✓]  │ │
│         │  │    Build an agent that classifies support tickets…     │ │
│         │  │    Score: 91%  ·  3 attempts  ·  18 min               │ │
│         │  │                              [View Results →]          │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ 2  Email Triage Pipeline                [Completed ✓]  │ │
│         │  │    Design an agent that triages inbound emails…        │ │
│         │  │    Score: 88%  ·  2 attempts  ·  14 min               │ │
│         │  │                              [View Results →]          │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ 3  Multi-Step Support Agent          [Exploring 🔥]    │ │
│         │  │    Build a multi-turn agent for escalation handling…   │ │
│         │  │    Gate progress  ████████░░  2/3 criteria             │ │
│         │  │    2 attempts · 4:02 active · 1 approach used         │ │
│         │  │                              [Resume Exercise →]       │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ 4  Agent Reliability Test           [Not Started]      │ │
│         │  │    Test your agent against adversarial inputs…         │ │
│         │  │    🔒 Complete exercise 3 first                        │ │
│         │  └────────────────────────────────────────────────────────┘ │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## Component breakdown

| Region | Component | Notes |
|--------|-----------|-------|
| Module header | `PageContainer` + inline progress | Module title, exercise count, overall progress bar |
| Module progress bar | `PFProgressBar` (module-level variant) | Fill: completed / total |
| Exercise rows | `ExerciseCard` (list variant) × N | Ordered list |
| Phase chip | `PFPhaseChip` (inline) | Each exercise row |
| Gate mini-bar | `PFProgressBar` (compact) | Only on `exploring` phase |
| CTA button | `Button` primary | "Resume Exercise →" (exploring) or "Start Exercise →" (not_started) or "View Results →" (completed) |
| Locked row | `ExerciseCard` locked | Dimmed + Lock icon + prerequisite label |

---

## Exercise card variants

### Completed
- `PFPhaseChip` phase=completed
- Score: `--text-sm` `--weight-medium`, score color (see EvalResultCard spec)
- Attempt count + active time summary
- CTA: "View Results →" (secondary ghost, navigates to results for best submission)

### Exploring (in-progress)
- `PFPhaseChip` phase=exploring + warm amber left-border accent (2px, `--color-pf-exploring`)
- Gate progress in compact `PFProgressBar` (single-line: "2/3 gate criteria met")
- Active time: formatted `h:mm` or `m:ss`
- Current approach count badge: "N approach(es) tried"
- CTA: "Resume Exercise →" (primary)

### Not Started (unlocked)
- `PFPhaseChip` phase=not_started
- Exercise prompt teaser (first 120 chars, truncated with "…")
- CTA: "Start Exercise →" (primary)

### Not Started (locked — prerequisite not met)
- Opacity 0.55
- `Lock` icon (16px) next to sequence number
- No prompt teaser
- Label: "Complete exercise [N] to unlock" in `--color-neutral-500`
- No CTA (row is non-interactive, `aria-disabled`)

### Fast-Unlocked (explored=false, phase=consolidation_unlocked or completed)
- `PFPhaseChip` fast-unlock variant + tooltip
- Small label below chip: "Exploration credit not earned"

---

## Module header

```
Module 2 · Tool Use & Orchestration
4 exercises · 2 of 4 complete

████████░░░░░░░░░░   2 / 4   50%
```

Module progress bar: `--progress-track-h` 8px; fill `--color-primary-500` for completed count. Label: `[n] / [total]` + percentage, tabular-nums.

---

## Module summary stats strip

Below the header, a compact 4-stat strip (horizontal, not cards — inline row):

| Stat | Value |
|------|-------|
| Completed | n of total |
| Exploring | n |
| Total attempts | Sum across module |
| Best score | Max mastery_score % |

Stat separator: `--color-neutral-200` vertical 1px rule. `--text-sm`, `--color-neutral-600`.

---

## States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| Loading | Page mount | Header skeleton + 4 `ExerciseCard` skeletons |
| All locked | User navigated directly but prerequisites not met | Show all locked state; "Return to Dashboard" link |
| All completed | Every exercise completed | Show celebration banner: "Module complete! Well done." |
| One in progress | Phase = exploring | Resume CTA highlighted in primary |

---

## Navigation

- Breadcrumb: `Dashboard / Modules / [Module Title]`
- "Back to Dashboard" link above module title (small, ghost, `ChevronLeft` icon)
- Each completed exercise: "View Results" navigates to `/exercises/[id]/results` (most recent EvaluationResult)
- Each in-progress: "Resume" navigates to `/exercises/[id]/challenge`
- Each not-started (unlocked): "Start" navigates to `/exercises/[id]/challenge`

---

## Accessibility notes

- Page `<h1>` = module title
- Exercise list: `<ol>` (ordered — sequence matters)
- Each exercise card: `<li>` containing `<article>`
- Locked exercises: `<li aria-disabled="true">` + `<span role="img" aria-label="Locked">🔒</span>`
- Module progress bar: `<progress value="2" max="4" aria-label="Module progress: 2 of 4 exercises complete">`
- PF gate criteria in compact bar: each criterion has accessible label
- Exploring phase time display: `<time>` element with `dateTime` attribute

---

## Responsive behaviour

- Exercise cards are always single-column (list layout)
- Module stats strip collapses to 2-column on <640px
- CTA buttons full-width on <640px
