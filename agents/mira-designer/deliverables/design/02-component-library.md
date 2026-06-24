# Mahir — Component Library Spec
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Status:** Accepted — feeds T-003 (wren-frontend)  
**Token source:** `03-tokens.css`

---

## Component index

| # | Component | Role |
|---|-----------|------|
| 1 | AppShell | Root layout wrapper |
| 2 | Sidebar | Primary navigation (both roles) |
| 3 | TopBar | App-wide header |
| 4 | PageContainer | Content area wrapper |
| 5 | Button | CTA / action |
| 6 | Badge | Status / label chip |
| 7 | PFPhaseChip | Productive Failure phase indicator |
| 8 | EvalStatusBadge | Submission evaluation status |
| 9 | PFProgressBar | Phase progress within an exercise |
| 10 | ModuleCard | Module summary card (dashboard) |
| 11 | ExerciseCard | Exercise row / card |
| 12 | KPIStrip | Stat strip (dashboard + cohort view) |
| 13 | ChallengeWorkspace | Full exercise workspace layout |
| 14 | BuildEditor | Code/prompt input editor |
| 15 | SubmissionPanel | Submit + async status panel |
| 16 | EvalResultCard | Evaluation result summary |
| 17 | ScenarioResultRow | Per-scenario pass/fail row |
| 18 | RubricScoreRow | Per-criterion rubric score row |
| 19 | PFSignalBadge | productive / low_effort / off_task signal |
| 20 | ConsolidationGate | Gate status + unlock reveal |
| 21 | CohortTable | Facilitator learner progress table |
| 22 | LearnerProgressRow | Single learner row in CohortTable |
| 23 | FacilitatorOverrideModal | Gate override confirmation |
| 24 | Input / Textarea | Form inputs |
| 25 | Alert | Inline contextual alerts |
| 26 | Modal | General modal shell |
| 27 | Skeleton | Loading placeholder |
| 28 | Toast | Global notification |
| 29 | Tooltip | Hover/focus descriptions |
| 30 | Tabs | Tab navigation |

---

## 1. AppShell

**Purpose:** Root layout — sidebar + topbar + content area.

**Props:**
```ts
interface AppShellProps {
  role: 'learner' | 'facilitator';
  sidebarCollapsed?: boolean;
  children: React.ReactNode;
}
```

**Layout:**
```
┌─────────────────────────────────────────────┐
│ TopBar (fixed, height: 56px)                │
├──────────┬──────────────────────────────────┤
│ Sidebar  │ Content area (scrollable)        │
│ 240px    │ max-width: 1280px, px-6          │
│ (fixed)  │                                  │
│          │                                  │
└──────────┴──────────────────────────────────┘
```

**Sidebar width:** `var(--sidebar-width)` (240px); collapses to `var(--sidebar-width-collapsed)` (64px) on `sidebarCollapsed=true`.  
**Content offset:** `margin-left: var(--sidebar-width)` + `padding-top: var(--topbar-height)`.  
**Background:** `var(--color-neutral-50)`.

---

## 2. Sidebar

**Purpose:** Primary navigation, always visible.

**States:** Expanded (240px) | Collapsed (64px, icon-only).

**Learner nav items:**
- Home / Dashboard (`/`)
- My Modules (`/modules`)
- Current Exercise (dynamic, if in progress)

**Facilitator nav items:**
- Cohort Overview (`/cohort`)
- Learner List (`/cohort/learners`)
- Modules (`/modules`)
- Reports (`/reports`)
- Settings (`/settings`) [org_admin only]

**Visual spec:**
- Background: `var(--sidebar-bg)` (`--color-primary-900`)
- Logo area: 56px height, matches TopBar
- Nav item height: 40px
- Nav item padding: 0 `var(--space-3)`
- Active item: `var(--sidebar-item-active-bg)` bg + left border 2px `var(--color-primary-400)` + text `var(--sidebar-text-active)`
- Hover: `var(--sidebar-item-hover-bg)`
- Icon: 20px Lucide, `var(--sidebar-text)` (75% white)
- Label: `var(--text-sm)`, `var(--sidebar-text)`
- Divider: `var(--sidebar-border)` 1px horizontal rule

**Accessibility:**
- `nav` element with `aria-label="Primary navigation"`
- Current page: `aria-current="page"` on active link
- Collapsed icons: `aria-label` on each anchor
- `role="separator"` on dividers

---

## 3. TopBar

**Purpose:** App-wide header — breadcrumb, user menu, workspace context.

**Height:** `var(--topbar-height)` (56px).  
**Background:** `var(--topbar-bg)` (white).  
**Border-bottom:** 1px `var(--topbar-border)`.

**Contents (left → right):**
- Sidebar toggle button (icon: `PanelLeft`, 36px touch target)
- Breadcrumb (`nav aria-label="Breadcrumb"`)
- Spacer (flex: 1)
- Cohort badge (current cohort name, `text-sm`, neutral-600)
- User avatar + display name (dropdown: Profile, Sign out)

---

## 4. PageContainer

**Purpose:** Consistent content area padding + max-width.

```ts
interface PageContainerProps {
  title?: string;
  description?: string;
  actions?: React.ReactNode;  // top-right CTA area
  children: React.ReactNode;
}
```

**Layout:**
```
┌─ PageContainer ─────────────────────────────┐
│ Page title (text-2xl, bold)  [Actions area] │
│ Description (text-base, neutral-600)        │
├─────────────────────────────────────────────┤
│ children                                    │
└─────────────────────────────────────────────┘
```

**Padding:** `var(--space-8)` top, `var(--content-padding-x)` horizontal.  
**Max-width:** `var(--content-max-width)`.

---

## 5. Button

**Variants:** `primary` | `secondary` | `ghost` | `danger`  
**Sizes:** `sm` (32px) | `md` (40px) | `lg` (48px)

**Visual spec:**

| Variant | Default bg | Default text | Border | Hover bg |
|---------|-----------|-------------|--------|---------|
| primary | `--color-primary-500` | white | none | `--color-primary-400` |
| secondary | white | `--color-neutral-800` | `--color-neutral-300` | `--color-neutral-100` |
| ghost | transparent | `--color-neutral-700` | none | `--color-neutral-100` |
| danger | `--color-error-500` | white | none | `--color-error-700` (darker) |

**States:** default, hover, active (scale 0.98), focus-visible (shadow ring), disabled (opacity 0.5, cursor not-allowed).

**Loading state:** `Loader2` icon (16px, spinning) replaces leading icon; text stays visible; button disabled.

**Props:**
```ts
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;   // leading icon
  iconRight?: React.ReactNode; // trailing icon
  type?: 'button' | 'submit';
  onClick?: () => void;
  children: React.ReactNode;
}
```

---

## 6. Badge

Generic status/label chip.

**Variants:** `default` | `primary` | `success` | `warning` | `error` | `info`

```
┌──────────────┐
│ ● Label text │   height: 20–24px, px-2, radius-sm
└──────────────┘
```

**Props:**
```ts
interface BadgeProps {
  variant?: 'default' | 'primary' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md';
  dot?: boolean;  // colored dot before label
  children: React.ReactNode;
}
```

---

## 7. PFPhaseChip

**Purpose:** Display current Productive Failure phase. The most important status element in learner UI.

```
┌─────────────────────┐
│ ● Exploring         │   height: 24px, px-2, radius-sm
└─────────────────────┘
```

**Props:**
```ts
type PFPhase = 'not_started' | 'exploring' | 'consolidation_unlocked' | 'completed';
interface PFPhaseChipProps {
  phase: PFPhase;
  explored?: boolean;    // if false and phase is unlocked, show fast-unlock variant
  showTooltip?: boolean; // default true
}
```

**Phase → visual mapping:**

| Phase | Dot color | Bg | Text |
|-------|-----------|-----|------|
| `not_started` | `--color-pf-not-started` | `--color-pf-not-started-bg` | `--color-pf-not-started-text` |
| `exploring` | `--color-pf-exploring` | `--color-pf-exploring-bg` | `--color-pf-exploring-text` |
| `consolidation_unlocked` (explored=true) | `--color-pf-unlocked` | `--color-pf-unlocked-bg` | `--color-pf-unlocked-text` |
| `consolidation_unlocked` (explored=false) | `--color-pf-fast` | `--color-pf-fast-bg` | `--color-pf-fast-text` |
| `completed` | `--color-pf-completed` | `--color-pf-completed-bg` | `--color-pf-completed-text` |

**Phase → label:**
- `not_started` → "Not Started"
- `exploring` → "Exploring"
- `consolidation_unlocked` + explored → "Solution Unlocked"
- `consolidation_unlocked` + !explored → "Fast Unlocked" (tooltip: "Unlocked early — exploration credit not earned")
- `completed` → "Completed"

**Accessibility:** `role="status"` + `aria-label="Exercise phase: [label]"`.

**Phase transition animation:** On phase change to `consolidation_unlocked`, apply a 350ms scale pulse (`scale(1.04) → scale(1)`) — the key emotional beat. Skip if `prefers-reduced-motion`.

---

## 8. EvalStatusBadge

**Purpose:** Submission evaluation lifecycle status.

```ts
type EvalStatus = 'queued' | 'running' | 'evaluated' | 'failed';
```

| Status | Icon | Color | Label |
|--------|------|-------|-------|
| `queued` | `Clock` | neutral-400 | "Queued" |
| `running` | `Loader2` (spin) | accent-500 | "Evaluating…" |
| `evaluated` | `CheckCircle2` | success-500 | "Evaluated" |
| `failed` | `XCircle` | error-500 | "Failed" |

**Accessibility:** `aria-live="polite"` wrapper when status changes; `role="status"`.

---

## 9. PFProgressBar

**Purpose:** Show gate criteria progress within a single exercise (attempts, approaches, time).

```
Gate progress          2/3 criteria met
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Genuine attempts    2 / 2
✓ Distinct approaches 2 / 2
  Exploration time    4:02 / 5:00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Props:**
```ts
interface PFProgressBarProps {
  attemptsGenuine: number;
  minAttempts: number;
  distinctApproaches: number;
  minDistinctApproaches: number;
  explorationSeconds: number;
  minExplorationSeconds: number;
  phase: PFPhase;
}
```

Each criterion row: label (left) + value fraction (right) + mini progress bar. Met criteria show `CheckCircle2` in success-500; unmet show `Circle` in neutral-400.

---

## 10. ModuleCard

**Purpose:** Summary card for a curriculum module on the learner dashboard.

```
┌──────────────────────────────────────────────┐
│ Module 1                             [Chip]  │
│ Foundations of AI Agents                     │
│ 4 exercises · Est. 3h                        │
│ ─────────────────────────────────────────── │
│ Progress ████████░░░░░░░░ 2/4 completed      │
└──────────────────────────────────────────────┘
```

**Props:**
```ts
interface ModuleCardProps {
  module: { id: string; title: string; sequenceIndex: number; summaryMarkdown: string; };
  exerciseCount: number;
  completedCount: number;
  currentPhase?: PFPhase; // phase of in-progress exercise
  onClick: () => void;
}
```

**Visual:** `var(--card-bg)`, `var(--card-shadow)`, `var(--card-radius)`. Module number prefix in `--color-primary-200` (small, top-left). Progress bar with `--color-pf-completed` fill. Hover: `--shadow-md` + border `--color-primary-200`.

---

## 11. ExerciseCard

**Purpose:** Exercise row within a module view.

```
┌────────────────────────────────────────────────────────┐
│ ● Exercise 1 · Ticket Classifier    [Exploring] [→]   │
│   Design an agent that classifies support tickets…    │
└────────────────────────────────────────────────────────┘
```

**Props:**
```ts
interface ExerciseCardProps {
  exercise: Exercise;
  progress?: ExerciseProgress;
  isLocked: boolean; // prerequisite not met
  onClick: () => void;
}
```

**Locked state:** Full row opacity 0.5; `Lock` icon; tooltip shows prerequisite name.

---

## 12. KPIStrip

**Purpose:** Top-of-page stat strip for dashboard (learner: personal stats) and cohort view (facilitator: aggregate stats).

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│   4/12   │ │    3     │ │   85%    │ │  12.5h   │
│ Exercises│ │ Exploring│ │ Gate Met │ │  Active  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
```

**Props:**
```ts
interface KPIStripProps {
  stats: Array<{
    value: string | number;
    label: string;
    delta?: string;       // e.g. "+2 this week"
    deltaPositive?: boolean;
    icon?: React.ReactNode;
  }>;
}
```

**Grid:** 4-column ≥1024px, 2-column 768–1023px, 1-column <768px.  
**Value:** `var(--text-3xl)`, `var(--weight-bold)`, `tabular-nums`.  
**Label:** `var(--text-sm)`, `var(--color-neutral-600)`.  
**Delta:** `var(--text-xs)`, positive = `--color-success-700`, negative = `--color-error-700`.

---

## 13. ChallengeWorkspace

**Purpose:** Full-screen layout for the agent-building exercise.

```
┌──────────────────────────────────────────────────────────┐
│ TopBar                                                   │
├──────────────────────────┬───────────────────────────────┤
│ Problem Panel (40%)      │ Build Panel (60%)            │
│                          │                              │
│ Exercise title           │ BuildEditor                  │
│ [PFPhaseChip]            │ (code/prompt input)          │
│                          │                              │
│ Problem statement        │ SubmissionPanel              │
│ (ill-structured, full)   │ [Submit button]              │
│                          │ [Async eval status]          │
│ Gate progress            │ [Past submissions list]      │
│ (PFProgressBar)          │                              │
│                          │ ─────────────────────────── │
│ [Consolidation gate      │ EvalResultCard               │
│  — locked or revealed]   │ (most recent result)         │
└──────────────────────────┴───────────────────────────────┘
```

**Layout split:** 40/60 on ≥1024px; stacked (build above problem) on <1024px.  
**Left panel:** `overflow-y: auto`, sticky to viewport height minus topbar.  
**Right panel:** `overflow-y: auto`.

**Critical:** Consolidation content in left panel is rendered only when `phase ∈ {consolidation_unlocked, completed}`. The component receives `consolidationContent` as `null` when locked — never pass locked content and hide it client-side.

---

## 14. BuildEditor

**Purpose:** Input area for the learner's agent build (prompt(s) + config + inline code).

```
┌─ Agent Build ─────────────────────────────────┐
│  [Tab: System Prompt] [Tab: User Prompt]      │
│  [Tab: Config] [Tab: Tools]                   │
│                                               │
│  ┌─────────────────────────────────────────┐ │
│  │  Code / prompt textarea                 │ │
│  │  (JetBrains Mono 14px, dark bg)         │ │
│  │  min-height: 280px                      │ │
│  └─────────────────────────────────────────┘ │
│                                               │
│  [Character count]          [Clear] [Format] │
└───────────────────────────────────────────────┘
```

**Props:**
```ts
interface BuildEditorProps {
  value: BuildPayload;
  onChange: (v: BuildPayload) => void;
  disabled?: boolean;         // true while submission is queued/running
  buildSpec: Exercise['build_spec'];  // constraints on what tabs are shown
}

interface BuildPayload {
  systemPrompt?: string;
  userPrompt?: string;
  config?: Record<string, unknown>;
  tools?: ToolDefinition[];
  inlineCode?: string;
}
```

**Accessibility:** Each tab panel is `role="tabpanel"`; textarea has `aria-label="[Tab name] for agent build"`.

---

## 15. SubmissionPanel

**Purpose:** Submit button + async status display + past submissions list.

```
┌──────────────────────────────────────────────┐
│ [Submit Agent]                  Attempt 3    │
├──────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────┐ │
│ │ ⏳ Evaluating your agent…               │ │
│ │   Sandbox running · Est. 30–60s         │ │
│ └──────────────────────────────────────────┘ │
├──────────────────────────────────────────────┤
│ Past submissions                             │
│  #3  [Evaluating]           just now        │
│  #2  [Evaluated] 78%        2 min ago       │
│  #1  [Evaluated] 52%        12 min ago      │
└──────────────────────────────────────────────┘
```

**States:**
- **Idle:** Submit button (primary, `md`). Shows attempt number.
- **Queued:** Button disabled + `Loader2` + "Queued…". EvalStatusBadge = queued.
- **Running:** Button disabled + "Evaluating your agent…" callout. EvalStatusBadge = running. Poll interval: 3s via SWR or React Query.
- **Evaluated:** Button re-enabled. EvalResultCard appears for latest result.
- **Failed:** Button re-enabled. Error alert: "Evaluation failed. Your code was queued — try resubmitting."

**Accessibility:** Status area has `aria-live="polite"`. Spinner has `aria-label="Evaluating"`.

---

## 16. EvalResultCard

**Purpose:** Structured display of the most recent EvaluationResult.

```
┌─ Evaluation Result ── Attempt 2 ─────────────────────────┐
│  [Evaluated]  78%  [productive]  Approach: single-prompt │
│                                                          │
│  Scenarios         3/4 passed                            │
│  ─────────────────────────────────────────────────────── │
│  ✓ Basic classification                                  │
│  ✓ Ambiguous ticket                                      │
│  ✓ Multi-language input                                  │
│  ✗ Edge case: empty payload            [Details ▼]       │
│                                                          │
│  Rubric                                                  │
│  ─────────────────────────────────────────────────────── │
│  ✓ Prompt clarity            ████████░░  0.8             │
│  ✓ Error handling            ████████████  1.0           │
│  ⚠ Edge case coverage        ████░░░░░░  0.4             │
│                                                          │
│  Feedback                                                │
│  "Your classification logic is solid, but the agent     │
│   fails on empty payloads. Try adding input validation…" │
└──────────────────────────────────────────────────────────┘
```

**Props:**
```ts
interface EvalResultCardProps {
  result: EvaluationResult;
  attemptNumber: number;
  collapsed?: boolean;   // summary-only for past submissions
}
```

**Score:** `--text-3xl`, `tabular-nums`, color by score: <50% = error-700, 50–79% = warning-700, ≥80% = success-700.  
**PFSignalBadge** (see #19) displayed prominently.

---

## 17. ScenarioResultRow

```ts
interface ScenarioResultRowProps {
  name: string;
  passed: boolean;
  detail?: string;  // expandable
}
```

`CheckCircle2` success-500 (passed) or `XCircle` error-500 (failed). Detail in collapsible `<details>`.

---

## 18. RubricScoreRow

```ts
interface RubricScoreRowProps {
  criterion: RubricCriterion;
  score: number;   // 0..1
  met: boolean;
  confidence: number;
  evidence?: string;
  severity?: string;
}
```

Mini inline progress bar (width proportional to score). Evidence text in `--font-mono` `--text-xs`.

---

## 19. PFSignalBadge

The PF signal is the core evaluation signal — display it prominently.

| Signal | Label | Icon | Color |
|--------|-------|------|-------|
| `productive` | "Productive" | `TrendingUp` | success |
| `low_effort` | "Low Effort" | `Minus` | warning |
| `off_task` | "Off Task" | `AlertTriangle` | error |

**Important:** Never label `low_effort` or `off_task` as "failure" in the UI — copy should be constructive. Use the signal badge alone; copy in the feedback_markdown does the explanation.

---

## 20. ConsolidationGate

**Purpose:** The critical gated content reveal — shows gate status when locked, canonical solution when unlocked.

**Locked state:**
```
┌──────────────────────────────────────────────┐
│  🔒 Canonical Solution                       │
│                                              │
│  Complete the gate requirements to unlock:  │
│  • 2 genuine attempts  ✓                    │
│  • 2 distinct approaches  ✗  (1/2)          │
│  • 5 min exploration  ✓                     │
│                                              │
│  [Facilitator override available]            │
└──────────────────────────────────────────────┘
```

**Unlocked state:**
```
┌──────────────────────────────────────────────┐
│  ✨ Solution Unlocked                        │
│  [Unlocked by: exploration gate | facilitator]│
│                                              │
│  [Markdown rendered canonical solution]      │
│                                              │
│  [Consolidation check questions, if present] │
└──────────────────────────────────────────────┘
```

**Props:**
```ts
interface ConsolidationGateProps {
  phase: PFPhase;
  explored: boolean;
  gateProgress: { attemptsGenuine: number; minAttempts: number; distinctApproaches: number; minDistinctApproaches: number; explorationSeconds: number; minExplorationSeconds: number; };
  consolidationContent: ConsolidationContent | null;  // null when locked
  facilitatorOverride?: { overriddenBy: string; reason: string; };
}
```

**Hard rule:** This component must never receive actual consolidation content when `phase` is `not_started` or `exploring`. The parent (API consumer) is responsible for not passing it; this component should also assert `if (phase not in ['consolidation_unlocked','completed']) return null` on the content render path.

---

## 21. CohortTable

**Purpose:** Facilitator view of all learners in a cohort — phase distribution, progress signals.

```
┌──────────────────────────────────────────────────────────────────┐
│ Filter: [All phases ▼] [Search learner…]            [Export CSV] │
├──────────┬────────────┬──────────┬──────────────┬───────────────┤
│ Learner  │ Module     │ Exercise │ Phase        │ Gate Progress │
├──────────┼────────────┼──────────┼──────────────┼───────────────┤
│ Ahmad R. │ Module 2   │ Ex. 3    │ [Exploring]  │ ████░░░ 2/3  │
│ Siti N.  │ Module 2   │ Ex. 2    │ [Completed]  │ 100%         │
│ Raj K.   │ Module 1   │ Ex. 4    │ [Not Started]│ —            │
└──────────┴────────────┴──────────┴──────────────┴───────────────┘
```

**Pagination:** 25 rows per page.  
**Sort:** all columns sortable. Default: last_activity desc.  
**Row click:** opens learner drill-down panel (slide-over at 480px).  
**Accessibility:** `<table>` with `<caption>`, `<th scope>`, `aria-sort`.

---

## 22. LearnerProgressRow

See CohortTable row spec. Inline `PFPhaseChip` + mini gate progress. `Loader2` spinner on `running` submission.

---

## 23. FacilitatorOverrideModal

**Purpose:** Confirmation modal for manually overriding a learner's PF gate.

```
┌─ Override Gate ──────────────────────────────┐
│  Learner: Ahmad Rashid                       │
│  Exercise: Ticket Classifier (Ex. 1-3)       │
│                                              │
│  ⚠ This action will unlock the canonical   │
│    solution for this learner immediately.   │
│    The action is logged and auditable.       │
│                                              │
│  Reason (required):                          │
│  ┌──────────────────────────────────────┐   │
│  │ Textarea…                            │   │
│  └──────────────────────────────────────┘   │
│                    [Cancel] [Override Gate]  │
└──────────────────────────────────────────────┘
```

**Validation:** Reason field minimum 10 characters. Submit = POST to `/cohort/{id}/overrides`.

---

## 24. Input / Textarea

Standard form inputs.

```ts
interface InputProps {
  label: string;
  error?: string;
  hint?: string;
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  required?: boolean;
  id: string;
}
```

**Label:** always visible `<label htmlFor>` — never placeholder-only.  
**Error:** `--color-error-500` border + error message below in `--color-error-700`.  
**Hint:** `--color-neutral-500` below label.  
**Focus:** `box-shadow: var(--focus-ring)`.

---

## 25. Alert

```ts
type AlertVariant = 'info' | 'success' | 'warning' | 'error';
interface AlertProps {
  variant: AlertVariant;
  title?: string;
  children: React.ReactNode;
  dismissible?: boolean;
}
```

Inline callout block. Left border 4px + icon + bg tint. `role="alert"` for errors/warnings; `role="status"` for info/success.

---

## 26. Modal

Standard dialog shell. `<dialog>` element with `aria-labelledby`, `aria-describedby`. Focus trap via `@radix-ui/react-dialog`. Backdrop: `rgba(0,0,0,0.4)` with `backdrop-filter: blur(2px)`. Max-width: 480px (sm), 640px (md), 800px (lg).

---

## 27. Skeleton

Loading placeholder. Animated shimmer (`background-size: 400% 100%` keyframe). Match the shape of the content it replaces. Respect `prefers-reduced-motion` (static gray block instead).

---

## 28. Toast

Global notification system (bottom-right). Max 3 visible. Auto-dismiss: 5s (info/success), 8s (warning), stays until dismissed (error). Stacked with `--space-2` gap.

```ts
type ToastVariant = 'info' | 'success' | 'warning' | 'error';
```

`aria-live="assertive"` for errors, `aria-live="polite"` for others.

---

## 29. Tooltip

`@radix-ui/react-tooltip`. Delay: 400ms open, 100ms close. Content: `--text-xs`, white on `--color-neutral-900`. Max-width: 240px. Never use tooltips as the only way to convey critical info.

---

## 30. Tabs

`@radix-ui/react-tabs`. Tab list: bottom border `--color-neutral-200`; active tab: bottom border 2px `--color-primary-500`; text `--color-primary-600`. `aria-selected` on active. Keyboard: arrow keys within `role="tablist"`.

---

## Radix primitives used

| Component | Radix primitive |
|-----------|----------------|
| Modal | `@radix-ui/react-dialog` |
| Tooltip | `@radix-ui/react-tooltip` |
| Tabs | `@radix-ui/react-tabs` |
| Dropdown (user menu) | `@radix-ui/react-dropdown-menu` |
| Select (filter dropdowns) | `@radix-ui/react-select` |
| Collapsible (scenario details) | `@radix-ui/react-collapsible` |

All Radix primitives provide keyboard navigation and ARIA handling by default — do not re-implement these.

---

## Component dependency map

```
AppShell
  └─ Sidebar, TopBar, PageContainer

ChallengeWorkspace
  ├─ BuildEditor
  ├─ SubmissionPanel
  │    └─ EvalStatusBadge, EvalResultCard
  │         ├─ ScenarioResultRow
  │         ├─ RubricScoreRow
  │         └─ PFSignalBadge
  ├─ ConsolidationGate
  │    └─ PFProgressBar
  └─ PFPhaseChip

CohortTable
  └─ LearnerProgressRow
       └─ PFPhaseChip, EvalStatusBadge

ModuleCard
  └─ PFPhaseChip
```
