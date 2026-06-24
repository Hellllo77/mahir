---
name: qa-check
description: Use to run the full quality bar from Section 7 of the Trainer-Agent
  brief against a completed cycle draft before it is delivered. Triggers on
  requests like "check this," "QA the draft," "is this ready," or after /draft-cycle
  completes. Also triggers when the owner asks whether a piece of content is good
  enough to use. Do not skip this step before delivering content — the cycle is
  not ready until every item passes.
allowed-tools: Read, Write
---

# QA Check Skill

Runs every quality bar item from the Trainer-Agent brief (Section 7) against a
cycle draft and returns a pass/fail report with specific notes. Nothing ships
until all items pass.

## When to Use

After `/draft-cycle $ARGUMENTS` completes. Available via `/qa-check $ARGUMENTS`.

## Process

### Step 1: Load the draft
Read `projects/$ARGUMENTS/cycle-draft.md`. Read the intake brief at
`projects/$ARGUMENTS/intake-brief.md`. Read `references/non-negotiables.md`.

### Step 2: Run substance checks
For each item, return **PASS** or **FAIL** with a one-sentence note.

**S1 — Specificity test:** Could a learner open their laptop and start the task
without further instruction?

**S2 — Predictability test:** Will the engineered failure actually happen when
the task is run — not just probably, but reliably?

**S3 — Stage-awareness test:** Does the evaluator name only the gap the next
cycle/component fixes — not a list of flaws, not a gap from a later cycle?

**S4 — No-loophole test:** Could the learner pass the success condition without
having learned the underlying lesson? If yes, the condition is too weak.

### Step 3: Run philosophy checks
**P1 — No-folder test:** Does any part of the content hand the learner a
template, definition, or finished component before they've felt the need for it?

**P2 — Vocabulary-follows-experience test:** Does any part teach a name or term
as the lesson, rather than a felt problem the term describes?

**P3 — Mental-model test:** Would a learner who completes this cycle leave
thinking "AI is magic" or "I just press a button"? If yes, the
manager-not-prompter framing has been lost.

### Step 4: Run audience checks
**Teen track — run if applicable:**

**A1 — Engagement test:** Is the scenario something a 15–17-year-old would
actually engage with — not what an adult thinks a teen would engage with?

**A2 — Language test:** Is the language age-appropriate without being
condescending?

**A3 — Safety check:** Is there anything in the scenario that could create a
safety, privacy, or age-appropriateness issue?

**Corporate track — run if applicable:**

**A4 — Realism test:** Is the scenario realistic enough that a working adult
recognises it as their actual job?

**A5 — Security test (Cycle 3 only):** Does the security failure catch a real
risk, not a hypothetical?

**A6 — Grant-readiness test:** Are learning outcomes documented in clear,
assessable language?

### Step 5: Compile and save the report
Write the QA report to `projects/$ARGUMENTS/qa-report.md`. Format:

```
## QA Report — [project name] — [date]

### Substance Checks
S1 Specificity: [PASS/FAIL] — [note]
S2 Predictability: [PASS/FAIL] — [note]
S3 Stage-awareness: [PASS/FAIL] — [note]
S4 No-loophole: [PASS/FAIL] — [note]

### Philosophy Checks
P1 No-folder: [PASS/FAIL] — [note]
P2 Vocabulary: [PASS/FAIL] — [note]
P3 Mental model: [PASS/FAIL] — [note]

### Audience Checks
[relevant items only]

### Verdict
[READY TO DELIVER — all items pass]
[NOT READY — N items failed: list them]

### Required fixes before delivery
[only if verdict is NOT READY]
```

Verify: every applicable check has a result. No item is skipped because "it's
obvious."

### Step 6: Report to owner
If all items pass: tell the owner the draft is ready to deliver.

If any items fail: present the failed items with the specific notes and suggest
running `/draft-cycle $ARGUMENTS --section [relevant-section]` to fix them.
Do not mark the cycle done until all items pass.
