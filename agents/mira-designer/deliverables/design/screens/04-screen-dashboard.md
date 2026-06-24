# Screen Spec: Learner Dashboard
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Route:** `/` (learner) · `/dashboard` (alias)  
**Role:** Learner

---

## Purpose

The learner's home base: shows cohort context, personal progress across all modules, and the current in-progress exercise CTA. Answers: "Where am I? What's next?"

---

## Wireframe

```
┌────────────────────────────────────────────────────────────────────────┐
│ TopBar: [≡] Mahir  /  Dashboard                 KrakenCorp Q3 · Ahmad │
├─────────┬──────────────────────────────────────────────────────────────┤
│ Sidebar │  Dashboard                                                   │
│         │                                                              │
│ ● Home  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│   Mods  │  │  4/12   │ │    2    │ │   83%   │ │  6.5h   │          │
│   Curr  │  │Exercises│ │Exploring│ │Gate Met │ │ Active  │          │
│         │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│         │                                                              │
│         │  ── Continue where you left off ─────────────────────────   │
│         │  ┌────────────────────────────────────────────────────────┐ │
│         │  │ Module 2 · Exercise 3                    [Exploring]   │ │
│         │  │ Multi-Step Customer Support Agent                      │ │
│         │  │ Gate progress  ████████░░  2/3 criteria · 4:02 active │ │
│         │  │                        [Resume Exercise →]             │ │
│         │  └────────────────────────────────────────────────────────┘ │
│         │                                                              │
│         │  ── Your Modules ────────────────────────────────────────   │
│         │  ┌──────────────────────────┐ ┌──────────────────────────┐  │
│         │  │ Module 1                 │ │ Module 2                 │  │
│         │  │ Foundations of AI Agents │ │ Tool Use & Orchestration │  │
│         │  │ 4 exercises · Est. 2h    │ │ 4 exercises · Est. 3h    │  │
│         │  │ ──────────────────────── │ │ ──────────────────────── │  │
│         │  │ ████████████ 4/4 done    │ │ ████████░░░░ 2/4 done   │  │
│         │  └──────────────────────────┘ └──────────────────────────┘  │
│         │  ┌──────────────────────────┐ ┌──────────────────────────┐  │
│         │  │ Module 3                 │ │ Module 4                 │  │
│         │  │ Evaluation & Reliability │ │ Production Agents        │  │
│         │  │ 4 exercises · Est. 3h    │ │ 4 exercises · Est. 4h    │  │
│         │  │ ──────────────────────── │ │ ──────────────────────── │  │
│         │  │ ░░░░░░░░░░░░  0/4 done   │ │ ░░░░░░░░░░░░  0/4 done  │  │
│         │  │ 🔒 Complete Module 2     │ │ 🔒 Complete Module 3    │  │
│         │  └──────────────────────────┘ └──────────────────────────┘  │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## Component breakdown

| Region | Component | Notes |
|--------|-----------|-------|
| Top KPI strip | `KPIStrip` | 4 stats: exercises done, currently exploring, gate met %, total active time |
| Resume card | Custom CTA card | Prominent, primary-100 bg, shows current exercise + gate progress |
| Resume button | `Button` variant=primary | "Resume Exercise →" |
| Module cards | `ModuleCard` × N | 2-column grid ≥768px, 1-column <768px |
| Locked module | `ModuleCard` locked variant | Opacity 0.6, Lock icon, prerequisite tooltip |

---

## KPI strip — stat definitions

| Stat | Value source | Label |
|------|-------------|-------|
| Exercises done | `ExerciseProgress` count where `phase = completed` / total assigned | "Exercises" |
| Exploring | `ExerciseProgress` count where `phase = exploring` | "In Progress" |
| Gate met % | Exercises where gate satisfied / total started | "Gate Met" |
| Active time | Sum of `exploration_seconds` across all `ExerciseProgress` | "Active" (formatted h:mm) |

---

## Resume CTA card

**Condition:** Rendered only if there is an exercise with `phase = exploring`.  
**Priority:** Most recently active exercise (sort by `ExerciseProgress.updated_at` desc).  
**Contents:**
- Module number + title (small, `--color-neutral-600`)
- Exercise title (`--text-xl`, `--weight-semibold`)
- `PFPhaseChip` phase=exploring
- `PFProgressBar` (compact, 3-row gate criteria)
- `Button` primary "Resume Exercise →"

**Visual:** Background `--color-primary-50`, border `--color-primary-200`, `--radius-lg`.

---

## Module card — locked state

Modules with unmet `prerequisite_exercise_ids` are locked:
- Full card opacity: 0.55
- Overlay icon: `Lock` 20px `--color-neutral-400`
- Bottom label: "Complete [prerequisite module name] to unlock"
- Not clickable (keyboard: `aria-disabled="true"` on the card link)

---

## Empty state (no modules assigned)

```
┌────────────────────────────────────────────┐
│  📋 No modules assigned                   │
│  Your facilitator hasn't started this     │
│  cohort yet. Check back soon.             │
└────────────────────────────────────────────┘
```

---

## States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| Loading | Initial page mount | `KPIStrip` skeleton (4 cards) + 2 `ModuleCard` skeletons |
| Active learner | ≥1 exercise in progress | Resume CTA card visible |
| All done | All exercises completed | Resume CTA hidden; celebration banner: "All exercises complete!" |
| No modules | Empty curriculum | Empty state (see above) |

---

## Accessibility notes

- Page `<h1>` = "Dashboard"
- `KPIStrip` stats: each card is `<article>` with `aria-label="[label]: [value]"` — not just decorative `<div>`
- Module cards: `<article role="link">` or `<a>` wrapping the card
- Locked cards: `aria-disabled="true"`, `tabIndex={-1}`, tooltip on focus explaining prerequisite
- Resume CTA: `<section aria-labelledby>` with h2 "Continue where you left off"

---

## Responsive behaviour

- **≥1024px:** 4-column KPI strip + 2-column module grid + sidebar expanded
- **768–1023px:** 2-column KPI strip + 2-column module grid + sidebar collapsed to icons
- **<768px:** 1-column everything + sidebar hidden (hamburger toggle)
