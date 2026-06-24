# Mahir — Design Direction
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Status:** Accepted — feeds T-003 (wren-frontend)

---

## 1. Brand rationale

Mahir (ماهر) means "skilled / proficient" in Malay and Arabic — the product name is the promise. The visual language must signal:

- **Credibility** — a product a corporate L&D manager presents to their CHRO without embarrassment.
- **Seriousness without sterility** — grant-funded, MY/SG corporate training context; not edgy, not childish, not generic SaaS.
- **Active learning** — the Productive Failure method rewards exploration and iteration; the UI must reinforce that _failing is not losing_.
- **Clarity under complexity** — async evaluation, multi-phase state, facilitator overrides; none of this should feel overwhelming.

The two client surfaces have distinct character:
- **Learner Web App** — focused workspace, step-by-step, encouraging. Reduce ambient complexity.
- **Facilitator Console** — data-dense, signal-rich, auditable. Respect professional expertise.

---

## 2. Color system

### Primary — Teal/Navy

Trustworthy, professional, regionally appropriate (teal is prominent in Malaysian institutional branding).

| Token | Value | Usage |
|-------|-------|-------|
| `--color-primary-950` | `#0a1628` | Deep navy — page backgrounds (dark mode only) |
| `--color-primary-900` | `#0f2341` | Dark navy — sidebar, top-bar |
| `--color-primary-800` | `#1a3a5c` | — |
| `--color-primary-700` | `#1e5480` | — |
| `--color-primary-600` | `#1a6fa3` | — |
| `--color-primary-500` | `#1b87c5` | Primary interactive — default button, links |
| `--color-primary-400` | `#3ba3dd` | Hover state |
| `--color-primary-300` | `#72bfe8` | Focus rings, active indicators |
| `--color-primary-200` | `#b0d9f3` | Subtle backgrounds |
| `--color-primary-100` | `#d8eef9` | Card highlight backgrounds |
| `--color-primary-50`  | `#eef7fd` | Page tint / light backgrounds |

### Accent — Amber

Energy, momentum, "currently active" state. Used sparingly.

| Token | Value | Usage |
|-------|-------|-------|
| `--color-accent-700` | `#92400e` | Text on light amber bg |
| `--color-accent-600` | `#b45309` | — |
| `--color-accent-500` | `#d97706` | Active/exploring phase, primary accent |
| `--color-accent-400` | `#f59e0b` | Hover |
| `--color-accent-100` | `#fef3c7` | Amber background |
| `--color-accent-50`  | `#fffbeb` | Amber tint |

### Neutral — Gray

Content backbone. Warm-shifted gray (not pure cool) to complement the teal primary.

| Token | Value | Usage |
|-------|-------|-------|
| `--color-neutral-950` | `#0c0d0f` | — |
| `--color-neutral-900` | `#111318` | Primary text |
| `--color-neutral-800` | `#1e2129` | Secondary text |
| `--color-neutral-700` | `#374151` | Tertiary text, icons |
| `--color-neutral-600` | `#4b5563` | Muted text |
| `--color-neutral-500` | `#6b7280` | Placeholder text |
| `--color-neutral-400` | `#9ca3af` | Disabled text |
| `--color-neutral-300` | `#d1d5db` | Dividers, borders |
| `--color-neutral-200` | `#e5e7eb` | Light borders |
| `--color-neutral-100` | `#f3f4f6` | Subtle backgrounds |
| `--color-neutral-50`  | `#f9fafb` | Page background |
| `--color-neutral-0`   | `#ffffff` | Card / surface |

### Semantic

| Token | Value | Usage |
|-------|-------|-------|
| `--color-success-700` | `#15803d` | Success text |
| `--color-success-500` | `#22c55e` | Success icon/border |
| `--color-success-100` | `#dcfce7` | Success background |
| `--color-success-50`  | `#f0fdf4` | Success tint |
| `--color-warning-700` | `#b45309` | Warning text |
| `--color-warning-500` | `#f59e0b` | Warning icon/border |
| `--color-warning-100` | `#fef3c7` | Warning background |
| `--color-error-700`   | `#b91c1c` | Error text |
| `--color-error-500`   | `#ef4444` | Error icon/border |
| `--color-error-100`   | `#fee2e2` | Error background |
| `--color-error-50`    | `#fef2f2` | Error tint |
| `--color-info-700`    | `#1d4ed8` | Info text |
| `--color-info-500`    | `#3b82f6` | Info icon/border |
| `--color-info-100`    | `#dbeafe` | Info background |

### Productive Failure phase palette

The PF phase is the most important UI signal in the learner surface. It must be instantly readable and emotionally accurate.

| Phase | Token | Color | Rationale |
|-------|-------|-------|-----------|
| `not_started` | `--color-pf-not-started` | `--color-neutral-300` (`#d1d5db`) | Neutral, no energy yet |
| `exploring` | `--color-pf-exploring` | `--color-accent-500` (`#d97706`) | Amber = active, warmth, movement |
| `consolidation_unlocked` | `--color-pf-unlocked` | `--color-primary-500` (`#1b87c5`) | Teal = breakthrough, the brand moment |
| `completed` | `--color-pf-completed` | `--color-success-500` (`#22c55e`) | Green = done, mastery confirmed |
| `fast_unlocked` (explored: false) | `--color-pf-fast` | `--color-neutral-400` (`#9ca3af`) | Desaturated — acknowledged but not rewarded |

---

## 3. Typography

**Primary typeface:** Inter (variable font) — system-native on most modern OS; falls back to the system-ui stack. Chosen for:
- Exceptional legibility at 11–14px (data tables, code-adjacent labels)
- Professional, neutral character — no personality clashes with corporate brand
- Full variable font (weight 100–900, optical sizing)

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
font-feature-settings: 'cv02', 'cv03', 'cv04', 'cv11';  /* improved numerals + disambiguous chars */
```

**Monospace** (code editors, submission payloads, agent build spec): `JetBrains Mono`, `Fira Code`, `Cascadia Code`, monospace.

### Type scale

| Token | Size | Line-height | Weight | Usage |
|-------|------|-------------|--------|-------|
| `--text-xs` | 11px | 1.45 | 400 | Labels, captions, table sub-values |
| `--text-sm` | 13px | 1.5 | 400 | Body small, table cells, secondary |
| `--text-base` | 15px | 1.6 | 400 | Body default, form inputs |
| `--text-md` | 16px | 1.5 | 500 | Body emphasis, card subtitles |
| `--text-lg` | 18px | 1.45 | 600 | Section headings, card titles |
| `--text-xl` | 22px | 1.35 | 600 | Page sub-headings |
| `--text-2xl` | 28px | 1.25 | 700 | Page titles |
| `--text-3xl` | 36px | 1.15 | 700 | Hero / KPI figures |
| `--text-mono-sm` | 12px | 1.6 | 400 | Code, submission JSON |
| `--text-mono-base` | 14px | 1.6 | 400 | Code editor |

---

## 4. Spacing

4px base unit. Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96.

```css
--space-1:  4px;
--space-2:  8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
--space-24: 96px;
```

---

## 5. Border radius

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 4px | Inputs, badges, chips |
| `--radius-md` | 8px | Cards, modals, popovers |
| `--radius-lg` | 12px | Large cards, panels |
| `--radius-full` | 9999px | Pill badges, avatar |

---

## 6. Shadows

Minimal, single-level shadow system. Flat with depth cues — enterprise feel, not consumer.

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-xs` | `0 1px 2px 0 rgba(0,0,0,0.05)` | Inputs, tight elements |
| `--shadow-sm` | `0 1px 3px 0 rgba(0,0,0,0.1), 0 1px 2px -1px rgba(0,0,0,0.1)` | Cards, default elevation |
| `--shadow-md` | `0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-lg` | `0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1)` | Toasts, floating panels |

---

## 7. Motion

Default to subtle, purposeful motion. Respect `prefers-reduced-motion`.

```css
--duration-fast:   100ms;
--duration-base:   200ms;
--duration-slow:   350ms;
--easing-default:  cubic-bezier(0.4, 0, 0.2, 1);
--easing-in:       cubic-bezier(0.4, 0, 1, 1);
--easing-out:      cubic-bezier(0, 0, 0.2, 1);
```

Phase transitions (e.g. exploring → consolidation_unlocked) may use a brief 350ms celebration pulse (`scale(1) → scale(1.04) → scale(1)`) on the phase chip. Gate-blocked-to-unlocked is the key emotional beat in the product.

---

## 8. Layout grid

- **AppShell:** fixed sidebar (240px) + fixed top-bar (56px) + scrollable content area
- **Content max-width:** 1280px, centered, with 24px horizontal padding
- **Sidebar collapsed:** 64px icon-only mode (facilitator console on smaller screens)
- **Grid for dashboard KPI strip:** 4-column on ≥1024px, 2-column on 768–1023px, 1-column on <768px
- **Responsive breakpoints:**

```css
--bp-sm:  640px;
--bp-md:  768px;
--bp-lg: 1024px;
--bp-xl: 1280px;
```

---

## 9. Iconography

Use **Lucide React** (stroke icons, 20px default, 16px dense, 24px large). Stroke width 1.5px. Never fill icons except for explicit "selected" states.

Key icons to reserve:
- `Brain` — Mahir logo mark / module icon
- `Beaker` / `FlaskConical` — challenge/exercise
- `CheckCircle2` — completed phase
- `Circle` — not_started phase
- `Loader2` (spinning) — evaluating/queued
- `Lightbulb` — consolidation unlocked
- `Users` — cohort / facilitator view
- `BarChart3` — progress / scores
- `ShieldCheck` — passed / gate satisfied
- `AlertTriangle` — warning / gate not met
- `ChevronRight` — drill-down / continuation

---

## 10. Tone of voice (UI copy)

| Context | Tone | Example |
|---------|------|---------|
| Exercise prompt | Direct, curious, no-hint | "Design an agent that classifies customer support tickets by priority. There is no single correct approach." |
| PF phase: exploring | Encouraging, no pressure | "Keep building. Exploration counts." |
| PF gate: not met yet | Honest, non-punishing | "2 of 3 gate criteria met. Try a different approach to unlock the solution." |
| PF gate: unlocked | Celebratory but professional | "Gate satisfied — canonical solution now available." |
| Evaluation: low_effort | Gentle, specific | "This submission didn't meet the minimum activity threshold. Expand your approach and resubmit." |
| Facilitator override | Formal, auditable | "Gate manually overridden by [facilitator]. Reason logged." |
| Error states | Clear, actionable | "Evaluation failed. Your code was queued — try resubmitting." |

Do not use: "Amazing!", "You got it!", "Oops!", gamification badges/XP/streaks. The corporate tone relies on earned respect, not manufactured enthusiasm.

---

## 11. PF-specific UI constraints (from architecture)

These are hard rules for wren-frontend, not suggestions:

1. **Never show consolidation content client-side until `ExerciseProgress.phase` is `consolidation_unlocked` or `completed`** — server-authoritative, not client-side logic.
2. **Submission status (`queued → running → evaluated → failed`) must be displayed honestly** — poll or subscribe and show live state. Do not optimistically assume `evaluated`.
3. **`explored: false` (fast_unlocked) must be visually distinct** from genuine exploration — use `--color-pf-fast` + a tooltip: "Unlocked early — consolidation available but exploration credit not earned."
4. **Evaluation loading state must be tolerant of latency** — sandbox + LLM judge takes seconds to minutes. Show `Loader2` spinner with "Evaluating your agent…" copy, not a fixed timeout message.
5. **Facilitator overrides must be surfaced in the learner view** — show "Unlocked by facilitator" label on any gate-overridden exercise.

---

## 12. Accessibility baseline

WCAG 2.2 AA minimum (EU Accessibility Act legally binding as of June 28, 2025).

- All text color/background pairs must meet 4.5:1 contrast ratio (text) or 3:1 (large text / UI components).
- All interactive elements have visible focus rings: `outline: 2px solid var(--color-primary-400); outline-offset: 2px;`
- Keyboard navigation complete — no mouse-only paths.
- Screen reader labels for all icon-only buttons (`aria-label`), status indicators (`aria-live` for async eval status), and phase chips (`role="status"`).
- Code editor areas: ensure `aria-label` on the textarea, announce submission state changes via `aria-live="polite"`.

Full a11y spec in `09-a11y-build-spec.md`.
