# Screen Spec: Cohort Progress View (Facilitator Console)
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Route:** `/cohort/[cohortId]` (Facilitator Console)  
**Role:** Facilitator · Org Admin

---

## Purpose

The facilitator's command view of the cohort. See all learners at a glance: who's exploring, who's stuck, who bypassed the gate (fast-unlock), where the cohort is distributed across phases. Surface actionable signals: learners who may need encouragement (stuck in `exploring` without recent activity), or who triggered `off_task` evaluations. Enable gate override with a single audited action.

---

## Wireframe

```
┌────────────────────────────────────────────────────────────────────────┐
│ TopBar: [≡] Mahir  /  Cohort  /  KrakenCorp Q3 2026         Farah ▾  │
├─────────┬──────────────────────────────────────────────────────────────┤
│ Sidebar │  KrakenCorp Q3 2026                                          │
│         │  Co-Worker · 18 learners · Started Jun 3                    │
│   Cohort│                                                              │
│    ●    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  Learn  │  │    6     │ │    8     │ │    3     │ │   1      │       │
│  Mods   │  │Completed │ │Exploring │ │ Not Start│ │  Stuck   │       │
│  Reports│  │exercises │ │          │ │          │ │ >2d idle │       │
│  Settgs │  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│         │                                                              │
│         │  ── Learner Progress ────────────────────────────────────   │
│         │                                                              │
│         │  Filter: [All phases ▼] [Module: All ▼] [Search…   ]       │
│         │  Sort: Last activity ▼         [Export CSV]                 │
│         │                                                              │
│         │  ┌────────┬──────────────┬────────────────┬──────┬────────┐ │
│         │  │Learner │ Current Exs  │ Phase          │ Gate │ Last   │ │
│         │  ├────────┼──────────────┼────────────────┼──────┼────────┤ │
│         │  │Ahmad R.│ M2 · Ex 3    │ [Exploring]    │ 2/3  │ 5m ago │ │
│         │  │ [→]    │              │                │ ████░│        │ │
│         │  ├────────┼──────────────┼────────────────┼──────┼────────┤ │
│         │  │Siti N. │ M2 · Ex 4    │ [Not Started]  │  —   │ 1h ago │ │
│         │  ├────────┼──────────────┼────────────────┼──────┼────────┤ │
│         │  │Raj K.  │ M1 · Ex 4    │ [Completed ✓] │ 3/3  │ 2h ago │ │
│         │  ├────────┼──────────────┼────────────────┼──────┼────────┤ │
│         │  │Mei L.  │ M2 · Ex 2    │ [Exploring 🔥]│ 1/3  │ 3d ago │ │
│         │  │ ⚠ Idle │              │                │ ██░░░│ stuck  │ │
│         │  ├────────┼──────────────┼────────────────┼──────┼────────┤ │
│         │  │Zaki A. │ M2 · Ex 3    │ [Fast Unlocked]│ —    │ 30m ago│ │
│         │  └────────┴──────────────┴────────────────┴──────┴────────┘ │
│         │  Showing 5 of 18 learners          [← 1  2  3  4 →]        │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## Component breakdown

| Region | Component | Notes |
|--------|-----------|-------|
| Cohort header | `PageContainer` + cohort metadata | Name, edition, learner count, start date |
| KPI strip | `KPIStrip` | 4 stats (see below) |
| Filter bar | `Select` + `Input` search + sort | Phase filter, module filter, name search |
| Learner table | `CohortTable` | See spec below |
| Learner rows | `LearnerProgressRow` | Phase chip, gate mini-bar, idle indicator |
| Pagination | Standard pagination | 25 rows/page default |
| Row CTA | Slide-over panel | Opens on row click — learner drill-down |

---

## KPI strip — facilitator stats

| Stat | Value source | Label |
|------|-------------|-------|
| Completed | Count of learners where all enrolled exercises completed | "Completed" |
| Exploring | Count of learners with ≥1 exercise `phase = exploring` | "Exploring" |
| Not started | Count of learners with 0 exercises started | "Not Started" |
| Stuck (idle >2 days) | Learners in `exploring` with `updated_at < now - 2 days` | "Needs Attention" (warning color) |

---

## CohortTable column spec

| Column | Width | Content | Sortable |
|--------|-------|---------|----------|
| Learner | 200px | `display_name` + email (small) | Y |
| Current Exercise | 180px | Module N · Exercise N | Y |
| Phase | 160px | `PFPhaseChip` | Y (by phase enum order) |
| Gate Progress | 120px | Mini gate bar + `n/3` fraction | Y (by n) |
| Last Activity | 100px | Relative timestamp | Y (default desc) |
| Actions | 64px | `[…]` overflow menu | N |

**Row height:** `var(--table-row-height)` (48px).  
**Hover:** `var(--table-row-hover)` (`--color-primary-50`).  
**Sticky header:** `position: sticky; top: 0;` inside table scroll container.

---

## Stuck learner row treatment

Condition: `phase = exploring` AND `ExerciseProgress.updated_at < now - 48h`.

- Row background: `--color-accent-50` (very faint amber)
- `⚠` icon (`AlertTriangle` 14px `--color-accent-600`) before learner name
- "Idle [N]d" label in last-activity column, `--color-accent-700`
- `[…]` menu includes "Send encouragement" (future feature, greyed out in pilot) and "Override gate"

---

## Fast-unlock row treatment

Condition: `ExerciseProgress.explored = false` + `phase ∈ {consolidation_unlocked, completed}`.

- `PFPhaseChip` fast-unlock variant (desaturated)
- Tooltip on chip: "Unlocked early — exploration credit not earned"
- Gate column: "—" (no gate criteria required; fast path taken)

---

## Overflow actions menu (`[…]`)

Per row:
```
View learner detail
View submissions
─────────────────────
Override gate          ← opens FacilitatorOverrideModal
─────────────────────
Withdraw from cohort   ← org_admin only
```

"Override gate" is always visible but disabled if `phase = completed` (nothing to override) or if a prior override already exists for this exercise.

---

## Learner drill-down slide-over

Opens on row click (or "View learner detail" in overflow menu). Slide-over at 480px from right edge. Overlay backdrop.

```
┌─ Ahmad Rashid ──────────────────────────────────── ×  ┐
│  ahmad.rashid@kraken.com.my                           │
│  Enrolled Jun 3 · Active                              │
│  ─────────────────────────────────────────────────── │
│  Exercise Progress                                     │
│  M1 Ex1  [Completed]  91%  3 attempts               │
│  M1 Ex2  [Completed]  88%  2 attempts               │
│  M1 Ex3  [Completed]  79%  4 attempts               │
│  M1 Ex4  [Completed]  95%  2 attempts               │
│  M2 Ex1  [Completed]  78%  3 attempts               │
│  M2 Ex2  [Completed]  92%  2 attempts               │
│  M2 Ex3  [Exploring]  —    2 attempts (gate 2/3)    │
│  ─────────────────────────────────────────────────── │
│  [Override Gate for M2 Ex3]                          │
└───────────────────────────────────────────────────────┘
```

- `ExerciseProgress` list: scrollable if long
- Per row: `PFPhaseChip` + score (or "—" if not evaluated) + attempt count
- "Override Gate" button: only active for the current in-progress exercise, only if gate not yet satisfied
- `Button` variant=secondary (not danger — override is legitimate, not destructive)

---

## FacilitatorOverrideModal interaction

Triggered from slide-over "Override Gate" or row overflow menu. See component spec #23.

On submit:
1. Modal closes
2. Row `PFPhaseChip` updates to `consolidation_unlocked`
3. Toast (info): "Gate overridden for [learner name] — [exercise name]. Action logged."
4. Slide-over (if open) refreshes the progress row

---

## Filter bar spec

```
[All phases ▼]  [Module: All ▼]  [Search learner…           ]  [Export CSV]
```

- Phase filter: `Select` — options: All phases, Not Started, Exploring, Solution Unlocked, Completed, Stuck
- Module filter: `Select` — options: All modules + each module by title
- Search: debounced 300ms, matches on `display_name` and `email`
- Export CSV: triggers `/api/cohorts/[id]/export` download — all learner progress data for the cohort. Org admin only.

---

## Cohort aggregate progress chart

Below the filter bar, a compact phase distribution bar:

```
Phase distribution (18 learners)
Completed  ████████████████░░░░░░░░░░░░░░░░  6 (33%)
Exploring  ████████████████████░░░░░░░░░░░░  8 (44%)
Not Started  ██████░░░░░░░░░░░░░░░░░░░░░░░░  3 (17%)
Stuck      ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1 (6%)
```

Horizontal stacked bar. Each phase uses its `--color-pf-*` color. Height 8px, `--radius-full`. Totals displayed as count + percentage. `<caption>` for accessibility.

---

## States

| State | Condition | Behaviour |
|-------|-----------|-----------|
| Loading | Page mount | KPI skeleton + table skeleton (8 rows) |
| Empty cohort | 0 enrolments | Empty state: "No learners enrolled. Invite learners via [Settings → Learners]." |
| All completed | All learners completed all exercises | Celebration banner: "Cohort complete!" |
| Active evaluation | Any learner submission `status = running` | Row shows `Loader2` spinner in phase column |
| Filter = no results | Search/filter returns 0 rows | Empty state in table: "No learners match this filter" + clear filter link |

---

## Facilitator Console sidebar differences

Facilitator sidebar shows different nav items than learner. This screen lives at `/cohort` under the Facilitator Console. The AppShell `role="facilitator"` prop switches the nav items (see component spec #2 Sidebar).

---

## Pagination

- 25 rows per page (matches `var(--table-row-height)` × 25 = comfortable scroll on 1080p)
- Total count shown: "Showing 1–25 of 18 learners" (or filtered count)
- Keyboard-accessible pagination controls

---

## Accessibility notes

- Page `<h1>` = cohort name
- `KPIStrip`: each stat is `<article aria-label="[label]: [value]">`
- Table: `<table>` with `<caption>` = "Learner progress for [cohort name]"; `<th scope="col">` for all column headers; `aria-sort` on sorted column
- Stuck rows: `aria-label` includes "Idle for [N] days" as part of the row label
- Phase chip in table: `role="status"` suppressed (too many announcements in a live table) — use `aria-label` on the cell instead
- Slide-over: `<dialog>` with focus trap; `aria-label="Learner detail: [name]"`; `aria-live="polite"` for the progress list update after gate override
- Export CSV button: `aria-label="Export cohort progress as CSV"`
- Override modal: `aria-labelledby` pointing to modal heading; reason textarea required with `aria-required="true"`

---

## Responsive behaviour

- Table is horizontally scrollable on <1024px (min-width: 700px enforced on table, scroll container wraps it)
- Slide-over becomes full-width bottom sheet on <640px
- KPI strip: 4-column ≥1024px, 2-column 640–1023px, 2-column <640px (always 2-column for facilitator — more data-dense)
- Export CSV button hidden on <640px (power user feature, mobile facilitator assumed rare)
