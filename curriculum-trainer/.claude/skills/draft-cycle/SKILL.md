---
name: draft-cycle
description: Use to produce a complete cycle or act deliverable in the 12-section
  format specified in the Trainer-Agent brief. Triggers after /intake has been
  completed and the owner has confirmed the proposal. Also triggers on requests
  like "draft the cycle," "write cycle 1," "write act 2 week 1," or "produce the
  content." Do not run without a confirmed intake brief — if one does not exist
  for this project, run /intake first. Supports --section [name] for targeted
  refinement of one section without redrafting the whole cycle.
allowed-tools: Read, Write
---

# Draft Cycle Skill

Produces the full 12-section cycle deliverable from the confirmed intake brief.
Evaluator scripts are always part of this skill — they are never drafted in
isolation, because the evaluator's stage-awareness depends on being coupled to
the failure mechanic.

## When to Use

After `/intake $ARGUMENTS` is complete and the owner has confirmed the proposal.
Available via `/draft-cycle $ARGUMENTS` or `/draft-cycle $ARGUMENTS --section
[section-name]` for targeted refinement.

## Supported Section Names (for --section flag)

`scenario` / `task` / `engineered-failure` / `evaluator` / `fix` /
`success-condition` / `materials` / `instructor-notes` / `outcomes` /
`research-sources` / `open-questions`

## Process

### Step 1: Load the intake brief
Read `projects/$ARGUMENTS/intake-brief.md`. Read `references/non-negotiables.md`.
Read `references/audience-levels.md` if this is a corporate session. Read
`templates/cycle-deliverable.md` for the required output structure.

If no intake brief exists, stop immediately. Tell the owner that `/intake
$ARGUMENTS` must be completed first, and suggest running it now.

### Step 2: Check for --section flag
If `--section [name]` is present, skip to the targeted section only (Step 4
variant). Do not redraft the whole cycle.

### Step 3: Draft the full cycle (all 12 sections)
Using the confirmed intake brief as the foundation, draft all 12 sections of
the cycle deliverable template. Follow the template structure exactly — do not
skip sections, do not add sections.

**Critical coupling rule:** The evaluator script (Section 6) must be drafted
with the engineered failure (Section 5) visible. The evaluator's reframing line
must specifically name the gap exposed by *this* failure mechanic — not a
generic gap. The stage-awareness rule must hold: the evaluator names only the
gap the next component fixes.

**Non-negotiable checks while drafting:**
- Does any part of the content hand the learner a template, definition, or
  finished component before they've felt the need? → Rewrite.
- Does any part teach a name as the lesson rather than a felt problem? → Rewrite.
- Does the success condition have a loophole — could a learner pass without
  learning the lesson? → Tighten it.
- Is the engineered failure *reliably* triggered by the task as written, or is
  it just probable? → If probable, redesign the task to make it certain.

Verify: all 12 sections are present. No section is empty or contains a
placeholder. The evaluator script names the gap from *this* cycle's failure
mechanic specifically.

### Step 4: Draft a targeted section (--section flag path)
Read the existing draft from `projects/$ARGUMENTS/cycle-draft.md`. Read the
relevant section. Redraft only that section, using the intake brief as the
grounding source. Apply the same non-negotiable checks relevant to that section.

Verify: the revised section is internally consistent with the failure mechanic
and the rest of the draft. The evaluator's stage-awareness is intact.

### Step 5: Self-QA pass
Before saving, run through these checks mentally:

- Could a learner open their laptop and start the task without further
  instruction? (Specificity test.)
- Will the engineered failure *actually* happen when the task is run, not
  just "probably"? (Predictability test.)
- Does the evaluator name only the gap the next cycle/component fixes?
  (Stage-awareness test.)
- Could the learner pass without having learned the lesson? (No-loophole test.)

If any check fails, fix before saving.

### Step 6: Save
Write the full draft to `projects/$ARGUMENTS/cycle-draft.md`. If a draft
already exists, version it (`cycle-draft-v2.md`, etc.) — do not overwrite.

Verify: file exists at the expected path. Read it back and confirm no template
placeholders remain and all 12 sections are populated.

### Step 7: Suggest next step
Tell the owner the draft is ready and suggest `/qa-check $ARGUMENTS` before
delivery.
