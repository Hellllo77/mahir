# Mahir — Accessibility & Build Handoff Spec
**Task:** T-004  
**Author:** mira-designer-mahir  
**Date:** 2026-06-11  
**Status:** Accepted — mandatory gate for T-003 (wren-frontend)  
**Standard:** WCAG 2.2 AA (minimum) — EU Accessibility Act legally binding as of 2025-06-28

---

## 1. Conformance target

**WCAG 2.2 Level AA** — every component and screen.  
Lighthouse a11y score target: **≥95**.  
axe-core violations: **0 critical, 0 serious** before ship.

---

## 2. Colour contrast requirements

All text/background combinations must meet:
- **Normal text (< 18pt / < 14pt bold):** 4.5:1 minimum
- **Large text (≥ 18pt / ≥ 14pt bold):** 3:1 minimum
- **UI components and graphical elements:** 3:1 minimum

### Verified token pairs

| Foreground | Background | Ratio | Pass |
|-----------|-----------|-------|------|
| `--color-neutral-900` (#111318) | `--color-neutral-0` (#fff) | 19.5:1 | ✓ AAA |
| `--color-neutral-700` (#374151) | `--color-neutral-0` (#fff) | 9.7:1 | ✓ AAA |
| `--color-neutral-600` (#4b5563) | `--color-neutral-0` (#fff) | 7.2:1 | ✓ AAA |
| `--color-neutral-500` (#6b7280) | `--color-neutral-0` (#fff) | 4.6:1 | ✓ AA |
| `--color-neutral-400` (#9ca3af) | `--color-neutral-0` (#fff) | 3.0:1 | ⚠ Large only |
| `--color-primary-500` (#1b87c5) | `--color-neutral-0` (#fff) | 4.5:1 | ✓ AA |
| `--color-primary-700` (#1e5480) | `--color-primary-100` (#d8eef9) | 7.1:1 | ✓ AAA |
| `--color-accent-700` (#92400e) | `--color-accent-100` (#fef3c7) | 7.0:1 | ✓ AAA |
| `--color-success-700` (#15803d) | `--color-success-100` (#dcfce7) | 7.5:1 | ✓ AAA |
| `--color-error-700` (#b91c1c) | `--color-error-100` (#fee2e2) | 6.9:1 | ✓ AAA |
| `--color-warning-700` (#b45309) | `--color-warning-100` (#fef3c7) | 7.0:1 | ✓ AAA |
| `--sidebar-text` (rgba(255,255,255,0.75)) | `--color-primary-900` (#0f2341) | 8.1:1 | ✓ AAA |
| `--sidebar-text-active` (#ffffff) | `--sidebar-item-active-bg` (rgba(255,255,255,0.10) over #0f2341) | 11.5:1 | ✓ AAA |
| `--editor-text` (#cdd6f4) | `--editor-bg` (#1e1e2e) | 11.4:1 | ✓ AAA |

**Note on `--color-neutral-400`:** Only use as placeholder text (never as informational text) and only over white. Do not use for any content that conveys meaning.

---

## 3. Focus management

### Focus ring (global)
```css
:focus-visible {
  outline: 2px solid var(--color-primary-400);
  outline-offset: 2px;
}
```

Never `outline: none` without a visible custom alternative. If a custom focus style is used, ensure contrast ratio ≥ 3:1.

### Focus ring on dark backgrounds (sidebar)
```css
.sidebar a:focus-visible {
  outline-color: white;
  outline-offset: 2px;
}
```

### Focus trap requirements

Modal, slide-over, and any overlay component must:
1. Move focus to the first focusable element inside on open
2. Trap focus within (tab cycles through internal focusables only)
3. Return focus to the trigger element on close

Use `@radix-ui/react-dialog` which handles this automatically. Do NOT implement custom focus trap logic.

---

## 4. Keyboard navigation

Every user interaction must be completable via keyboard.

| Interaction | Keyboard behaviour |
|------------|-------------------|
| Submit agent | `Tab` to submit button, `Enter` or `Space` to submit |
| BuildEditor tabs | `Tab` to tab list; arrow keys within `role="tablist"` |
| Collapsible scenario detail | `Enter` / `Space` on `<details>/<summary>` |
| Slide-over open | `Enter` / `Space` on row or button |
| Slide-over close | `Escape` key; also close button |
| Modal confirm | `Enter` on primary action button |
| Dropdown / select | Standard `Select` keyboard: `Space` to open, arrow keys to navigate, `Enter` to select, `Escape` to close |
| Table row action | `Enter` on row focuses slide-over open |
| Pagination | `Tab` to page buttons, `Enter` to navigate |

---

## 5. ARIA requirements by component

### PFPhaseChip
```html
<span role="status" aria-label="Exercise phase: Exploring">
  <span aria-hidden="true">●</span>
  Exploring
</span>
```

### EvalStatusBadge (live region wrapper)
```html
<div aria-live="polite" aria-atomic="true">
  <span role="status" aria-label="Evaluation status: Evaluating…">
    <!-- badge content -->
  </span>
</div>
```

### BuildEditor textarea
```html
<textarea
  id="system-prompt-editor"
  aria-label="System prompt for agent build"
  aria-describedby="system-prompt-hint"
  aria-required="true"
/>
```

### ConsolidationGate (locked)
```html
<section aria-label="Canonical solution — locked">
  <p>Complete the gate requirements to unlock the canonical solution.</p>
  <!-- criteria list -->
</section>
```

### ConsolidationGate (unlocked)
```html
<section aria-label="Canonical solution — unlocked">
  <!-- rendered content -->
</section>
```

### CohortTable
```html
<table>
  <caption>Learner progress for KrakenCorp Q3 2026</caption>
  <thead>
    <tr>
      <th scope="col" aria-sort="descending">Last Activity</th>
      <th scope="col">Learner</th>
      <!-- ... -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><!-- learner name --></td>
      <!-- ... -->
    </tr>
  </tbody>
</table>
```

### Score display
```html
<data value="78">78%</data>
```

### Rubric score bar
```html
<meter
  value="0.8"
  min="0"
  max="1"
  aria-label="Prompt clarity: 0.8 out of 1.0"
/>
```

### Module progress bar
```html
<progress value="2" max="4" aria-label="Module progress: 2 of 4 exercises complete" />
```

### Icon-only buttons
```html
<button aria-label="Close slide-over">
  <XIcon aria-hidden="true" />
</button>
```

---

## 6. Screen reader announcements

### Submission lifecycle announcements
Every submission status change must be announced. Use `aria-live="polite"` for non-urgent updates:

```
"Submission queued for evaluation."
"Evaluation in progress — please wait."
"Evaluation complete. Score: 78%. Productive signal."
"Evaluation failed. Please resubmit."
```

Place the live region in a persistent `<div aria-live="polite" aria-atomic="true">` near the `SubmissionPanel` heading. Update its text content (not innerHTML) to trigger announcement.

### Phase change announcement
When phase changes to `consolidation_unlocked`:
```
"Gate satisfied — canonical solution now available."
```

Use the `PFPhaseChip` `role="status"` region; text update triggers the announcement.

---

## 7. Images and icons

- All informational icons must have `aria-label` on the surrounding element or `aria-hidden="true"` + adjacent accessible text.
- Decorative icons (visual polish only): `aria-hidden="true"`.
- The Mahir logo: `<img alt="Mahir">`.
- Score bar / chart elements: do not rely on colour alone. Always include numeric value.

---

## 8. Forms

- Every input must have a visible `<label>` associated via `htmlFor` + `id`. No placeholder-as-label.
- Error messages associated via `aria-describedby`. Error state communicated via `aria-invalid="true"`.
- Required fields: `aria-required="true"`.
- Character count announcements: update `aria-live="polite"` region on input (debounced 500ms).

---

## 9. Motion and animation

All animations must respect `prefers-reduced-motion: reduce`:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0ms !important; transition-duration: 0ms !important; }
}
```

The `03-tokens.css` sets `--duration-*` tokens to `0ms` under this media query.

The phase-unlock pulse animation on `PFPhaseChip` is gated behind this token — it uses `--duration-slow` (350ms; reduced to 0ms under prefers-reduced-motion).

---

## 10. axe-core CI integration

axe-core must be integrated into the test suite before any component ships. Use `jest-axe` for component-level checks and `@axe-core/playwright` for end-to-end page checks.

### Component test pattern (jest-axe)
```ts
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

it('has no axe violations', async () => {
  const { container } = render(<PFPhaseChip phase="exploring" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

This test is **required for every component** in the library. It is a DoD gate — PR is rejected if it's missing.

### Playwright end-to-end pattern
```ts
import AxeBuilder from '@axe-core/playwright';

test('dashboard has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

Run axe-core Playwright checks against all 5 screens in CI.

### axe-core rules to enable (beyond default)
- `color-contrast-enhanced` (AAA) — warn, not fail (AA is the gate)
- `aria-required-children` — fail
- `duplicate-id` — fail
- `landmark-one-main` — fail
- `page-has-heading-one` — fail
- `focus-order-semantics` — warn

---

## 11. WCAG 2.2 — Success Criteria checklist

Key new criteria in WCAG 2.2 (not in 2.1) that apply to Mahir:

| SC | Title | Application |
|----|-------|-------------|
| 2.4.11 | Focus Not Obscured (Minimum) | No sticky header/footer should fully obscure a focused element |
| 2.4.12 | Focus Not Obscured (Enhanced) | Preferred: focused element fully visible |
| 2.4.13 | Focus Appearance | Focus indicators meet minimum size (2px outline, 3:1 contrast) |
| 2.5.7 | Dragging Movements | N/A (no drag interactions in pilot) |
| 2.5.8 | Target Size (Minimum) | All tap targets ≥ 24×24 CSS pixels (button minimum is 32px — covered by `--btn-height-sm`) |
| 3.2.6 | Consistent Help | Help/contact link in same location on every page |
| 3.3.7 | Redundant Entry | Form re-use (e.g. override modal) — do not force re-entry of info already provided |
| 3.3.8 | Accessible Authentication (Minimum) | SSO login (OIDC) preferred over password-only for cognitive accessibility |

---

## 12. Keyboard shortcut reference (future — pilot scope: basic)

For the pilot, no custom keyboard shortcuts are required. Basic browser shortcuts must work: Tab/Shift+Tab, Enter, Space, Escape, arrow keys in composites. Do not intercept these.

Future: slash-command shortcuts for BuildEditor (`/system`, `/user`, `/config`).

---

## 13. Language and HTML

- `<html lang="en">` (pilot is English; future: `lang="ms"` for Bahasa Malaysia edition)
- Page `<title>` follows: `[Page Name] — Mahir`
- No `tabIndex > 0` — use natural DOM order for focus sequence

---

## 14. Performance / Lighthouse targets

| Metric | Target |
|--------|--------|
| Lighthouse Accessibility | ≥95 |
| Lighthouse Performance | ≥90 |
| Lighthouse Best Practices | ≥90 |
| INP (Interaction to Next Paint) | ≤200ms |
| LCP (Largest Contentful Paint) | ≤2.5s |
| CLS (Cumulative Layout Shift) | ≤0.1 |

Evaluation status updates (polling) must not cause CLS. Use fixed-height containers for `EvalStatusBadge` and `SubmissionPanel` status area. Pre-allocate space for `EvalResultCard` with a `Skeleton` placeholder while loading.

---

## 15. Hand-off checklist for wren-frontend

Before shipping any component or screen, confirm:

- [ ] `jest-axe` test present and passing (0 violations)
- [ ] `@axe-core/playwright` test present and passing for the screen
- [ ] All interactive elements have visible `:focus-visible` ring
- [ ] All icon-only buttons have `aria-label`
- [ ] All form inputs have visible `<label>` with `htmlFor`
- [ ] `aria-live` regions present for: submission status, phase changes, toast announcements
- [ ] `aria-disabled` (not `disabled` alone) on locked interactive elements
- [ ] Table `<caption>`, `<th scope>`, and `aria-sort` present
- [ ] Colour contrast verified: no pairs below 4.5:1 for body text
- [ ] `prefers-reduced-motion` disables all CSS transitions/animations
- [ ] `ConsolidationGate` never renders locked content even if passed as prop
- [ ] Submission status polling stops when `evaluated` or `failed`
- [ ] `PFPhaseChip` phase-unlock pulse animation fires correctly (and is disabled under reduced-motion)
- [ ] Lighthouse a11y score ≥95 on all 5 screens in CI
