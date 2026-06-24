# Screen Spec: Agent-Building Challenge Interface
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Route:** `/exercises/[exerciseId]/challenge`  
**Role:** Learner

---

## Purpose

The core workspace where the learner builds and submits their agent. The most complex screen in the product. Must surface async evaluation status honestly, reflect PF phase truthfully, and never leak consolidation content client-side before the gate passes.

---

## Wireframe (≥1024px — split layout)

```
┌────────────────────────────────────────────────────────────────────────┐
│ TopBar: [≡] Mahir  /  Module 2  /  Exercise 3                 Ahmad ▾ │
├─────────┬──────────────────────────────────────────────────────────────┤
│         │  ┌─────────────────────────────┐ ┌──────────────────────────┐│
│ Sidebar │  │  PROBLEM  (40%)             │ │  BUILD  (60%)            ││
│         │  │                             │ │                          ││
│         │  │  Multi-Step Support Agent   │ │  ┌─── Agent Build ─────┐ ││
│         │  │  [Exploring 🔥]             │ │  │ [System] [User] [Cfg]│ ││
│         │  │                             │ │  │                      │ ││
│         │  │  Build a multi-turn agent   │ │  │  textarea (dark bg)  │ ││
│         │  │  that handles escalation    │ │  │  min-h: 280px        │ ││
│         │  │  in customer support        │ │  │                      │ ││
│         │  │  workflows. The agent must  │ │  │  [chars: 0/4000]     │ ││
│         │  │  decide when to escalate,   │ │  └──────────────────────┘ ││
│         │  │  collect context, and route │ │                          ││
│         │  │  to the right team.         │ │  [Submit Agent]  Attempt 3││
│         │  │                             │ │                          ││
│         │  │  ── Gate Progress ───────   │ │  ─────────────────────── ││
│         │  │  2/3 criteria met           │ │                          ││
│         │  │  ✓ 2 genuine attempts       │ │  ┌──────────────────────┐ ││
│         │  │  ✗ 2 distinct approaches    │ │  │ ⏳ Evaluating…       │ ││
│         │  │    (1/2 · try another way)  │ │  │ Sandbox running      │ ││
│         │  │  ✓ 5 min exploration        │ │  │ Est. 30–60s          │ ││
│         │  │                             │ │  └──────────────────────┘ ││
│         │  │  ── Canonical Solution ───  │ │                          ││
│         │  │  ┌─────────────────────┐   │ │  ── Past Submissions ───  ││
│         │  │  │ 🔒 Locked           │   │ │  #3  [Evaluating]  now   ││
│         │  │  │ Unlock requirements:│   │ │  #2  [Evaluated] 78% 2m  ││
│         │  │  │ • Approaches 1/2   │   │ │  #1  [Evaluated] 52% 12m ││
│         │  │  └─────────────────────┘   │ │                          ││
│         │  └─────────────────────────────┘ └──────────────────────────┘│
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## Layout spec

**Split panel:** 40% problem / 60% build. Both panels scroll independently.  
**Sticky header in left panel:** Exercise title + `PFPhaseChip` sticky to top of left panel as you scroll the problem.  
**No page-level scroll** — each panel handles its own scroll.  
**Stack on <1024px:** build panel above problem panel (learner types first, reads below).

---

## Left panel: Problem

### Exercise header (sticky)
```
Multi-Step Support Agent          [Exploring 🔥]
Module 2 · Exercise 3
```
- Title: `--text-xl`, `--weight-semibold`
- `PFPhaseChip` right-aligned
- Module breadcrumb: `--text-sm`, `--color-neutral-600`
- Sticky: `position: sticky; top: 0; background: var(--card-bg); z-index: var(--z-raised);`

### Problem statement
Full `prompt_markdown` rendered via `react-markdown` with `remark-gfm`.  
Font: `--text-base`, line-height: `--leading-relaxed`.  
Max content width: 520px within the panel.  
**Important:** No hints, no sample solutions, no approach suggestions in this panel — only what the `Exercise.prompt_markdown` contains.

### Gate progress
`PFProgressBar` (full variant — shows all 3 criteria rows).  
Visible only when `phase = exploring`.  
Heading: `--text-sm`, `--weight-semibold`, `--color-neutral-700`: "Gate progress — [n]/3 criteria met"

### ConsolidationGate
Below gate progress. Renders:
- **`phase = not_started | exploring`:** Locked state (gate requirements list).
- **`phase = consolidation_unlocked | completed`:** Canonical solution revealed + check questions if present.

**Hard rule:** `consolidationContent` prop is `null` when locked. Component renders only the locked UI. This is enforced at the API consumer layer — the challenge page fetches consolidation content only after confirming phase server-side.

---

## Right panel: Build

### BuildEditor
Tabs: System Prompt · User Prompt · Config · Tools (tabs shown per `build_spec`).  
Editor: `--editor-bg`, `--editor-font`, `--editor-font-size`. Line numbers shown.  
Character count: bottom-right of editor frame, `--text-xs`, `--color-neutral-500`.  
Disabled (opacity 0.6, no cursor) when submission is `queued` or `running`.

### Submit button + attempt counter
```
[Submit Agent]          Attempt 3 of ∞
```
- Button: `Button` variant=primary size=md, full-width
- `Loader2` spinner replaces button text while loading (`queued` / `running`)
- Attempt counter: `--text-sm`, `--color-neutral-500`, right-aligned

**Disabled conditions:**
- While `queued` or `running`
- If `BuildEditor` content is empty / below minimum length (show tooltip: "Add your agent build before submitting")

### Evaluation status callout
Shown when latest submission is `queued` or `running`:
```
┌────────────────────────────────────────────┐
│  ⏳ Evaluating your agent…               │
│  The sandbox is running your agent        │
│  against test scenarios. This usually     │
│  takes 30–60 seconds.                     │
└────────────────────────────────────────────┘
```
- `Alert` variant=info
- `aria-live="polite"` wrapper
- Progress: indeterminate spinner (`Loader2` 20px `--color-accent-500`, spinning)

**On failure (`status = failed`):**
```
┌────────────────────────────────────────────┐
│  ✗ Evaluation failed                      │
│  Your agent was queued but the evaluation │
│  service encountered an error. Resubmit   │
│  to try again — your code is preserved.   │
└────────────────────────────────────────────┘
```
- `Alert` variant=error

### EvalResultCard (latest result)
Shown when latest submission is `evaluated`. See component spec #16.  
Collapsed by default for attempts 1…n-1. Latest result expanded by default.

### Past submissions list
Compact list of previous submissions:
```
#3  [Evaluating…]                    just now
#2  [Evaluated]  78%  productive     2 min ago
#1  [Evaluated]  52%  productive     12 min ago
```
- Row click → expand inline `EvalResultCard` (collapsed=true variant)
- `EvalStatusBadge` + score (color-coded) + `PFSignalBadge` (compact) + relative timestamp
- `--text-sm`; row hover: `--color-primary-50`

---

## Phase transitions

### `exploring` → `consolidation_unlocked` (gate satisfied)

Trigger: page receives `evaluation.completed` event and `ExerciseProgress.phase` changes.

1. `PFPhaseChip` updates from amber → teal with 350ms scale pulse
2. Toast (success): "Gate satisfied — canonical solution now available"
3. Left panel `ConsolidationGate` animates from locked → unlocked state (fade in, `--duration-slow`)
4. Page title updates

This is the key emotional beat of the product — the animation budget is justified.

### `not_started` → `exploring` (first submit)

1. `PFPhaseChip` updates from gray → amber
2. `PFProgressBar` appears in left panel (fade-in)
3. No toast (too early to celebrate)

---

## Polling / real-time

Evaluation status polling: **SWR** with `refreshInterval: 3000` on `GET /submissions/[id]/status` when `status ∈ {queued, running}`. Stop polling when `status ∈ {evaluated, failed}`.

ExerciseProgress polling: **SWR** with `refreshInterval: 5000` when `phase = exploring`. Stop when `phase = consolidation_unlocked | completed`.

---

## URL + navigation

- Navigated here from module view "Resume Exercise" / "Start Exercise" buttons
- TopBar breadcrumb: `Dashboard / Module 2 / Exercise 3`
- No "back" in the browser sense — breadcrumb is canonical navigation
- On completion (`phase = completed`): optional "View Results" secondary CTA appears above the build panel, linking to `/exercises/[id]/results`

---

## States summary

| State | Key signals | UI impact |
|-------|------------|-----------|
| Not started | `phase = not_started`, no submissions | Submit button active; no gate progress; ConsolidationGate locked, no criteria shown yet |
| Exploring — idle | `phase = exploring`, no active submission | Submit active; gate progress visible; ConsolidationGate locked |
| Exploring — queued | Latest submission `status = queued` | Submit disabled, callout: "Queued…" |
| Exploring — running | Latest submission `status = running` | Submit disabled, callout: "Evaluating…" |
| Exploring — just evaluated | Latest submission `status = evaluated` | Submit re-enabled; EvalResultCard shown; gate progress updated |
| Exploring — eval failed | Latest submission `status = failed` | Submit re-enabled; error alert |
| Consolidation unlocked | `phase = consolidation_unlocked` | PFPhaseChip teal; ConsolidationGate reveals canonical solution |
| Completed | `phase = completed` | PFPhaseChip green; results available |

---

## Accessibility notes

- `<main>` contains two `<section>` elements: "Problem" (`aria-label="Exercise problem"`) and "Build" (`aria-label="Agent build workspace"`)
- `BuildEditor` textarea: `aria-label="System prompt for agent build"` (or appropriate tab label)
- Evaluation status: `aria-live="polite"` region — updates announced on submission status change
- Gate progress: each criterion row has `role="listitem"` with `aria-label="[criterion]: [met/not met]"`
- Phase chip: `role="status"` — announced on phase change
- Submit button: `aria-disabled` when not submittable + `aria-describedby` pointing to reason
- `ConsolidationGate` locked: `aria-hidden` on locked icon; meaningful text label "Canonical solution locked until gate criteria met"
- Keyboard: tab order follows visual left-to-right in split layout; on mobile (stacked) follows DOM order (build first)
