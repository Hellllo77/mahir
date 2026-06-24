---
name: intake
description: Use at the start of every content-creation session, before any cycle
  drafting begins. Triggers on any request to create, draft, or start a new cycle,
  act, scenario, evaluator script, or piece of curriculum content. Also triggers
  when the user names a track (teen/corporate), an act or cycle number, an industry,
  or an audience. Do not wait for the user to invoke intake by name — trigger on
  the intent to produce content. This skill is mandatory before /draft-cycle runs.
  If called without sufficient parameters, ask for them.
allowed-tools: Read, Write, WebSearch, WebFetch
---

# Intake Skill

Collects context, researches the industry/situation, flags dependencies, and
produces a confirmed evidence brief and proposal — in that order. Full cycle
drafting cannot begin until intake is complete and the owner has confirmed the
proposal.

## When to Use

Triggered automatically whenever a content-creation session begins. Also
available manually via `/intake $ARGUMENTS` where `$ARGUMENTS` names the
project (e.g. `corporate-cycle1-manufacturing-management`).

## Process

### Step 1: Load context
Read `references/lessons-learned.md` for prior learnings relevant to this
session. Read `references/non-negotiables.md` to prime the non-negotiable
checks. Read `references/cycle-engine.md` for the engine structure.

### Step 2: Collect track and parameters

Ask the owner to confirm:

**All sessions:**
- Track: Teen ("Build Your AI Co-Founder") or Corporate ("Build Your AI
  Co-Worker")?
- Which cycle or act/week is being designed?

**Corporate sessions only (all three are required):**
- Industry context: what industry is this cohort in? (No pre-built files —
  research will be performed fresh.)
- Audience level: Management / Admin & Back-office / Frontline & Operations /
  Specialist-IC? (See `references/audience-levels.md`.)
- Process type: which process from the controlled menu? (Recurring report /
  content drafting / research or lookup / intake processing.) If the owner
  names a process not on the menu, flag it and discuss before proceeding.

Do not proceed to Step 3 until all required parameters are confirmed.

### Step 3: Flag unresolved dependencies
Before researching, check whether the content being requested has an unresolved
dependency:

- **Teen track:** Is the venture scenario locked? If not, and the owner is
  requesting content that depends on it (any concrete weekly task), stop and
  surface this. Do not draft content built on a guessed scenario.
- **Corporate track:** Is the process type confirmed and specific enough to
  engineer predictable failure moments? If not, stop and surface this.

If a dependency is unresolved, present the options and wait for a decision
before continuing.

Verify: no unresolved dependency exists before proceeding to research.

### Step 4: Research the context
Run `/research` for the confirmed industry and process type (corporate), or for
the venture context (teen). Minimum research targets:

- What does this process/context actually look like in this industry?
- What are the realistic failure modes of AI in this specific context?
- What vocabulary does this audience use for this work?
- What would "real business standards" mean for the evaluator in this context?

Compile findings into a short evidence brief (half a page). This brief is the
research foundation — the proposal must reference it.

Verify: evidence brief contains at least one concrete industry-specific finding
per research target above. No claim in the brief is invented or pulled from
training priors without a search to verify it.

### Step 5: Produce the proposal
Write a proposal (roughly half a page) covering:

- The scenario: the concrete situation the learner is in
- The engineered failure: which weakness, and the specific mechanism
- The rough shape of the evaluator's reframing
- Key choices being made and why, grounded in the evidence brief
- Any open questions that need the owner's input

Present the proposal to the owner and wait for their reaction. Do not begin
drafting the full cycle until the owner confirms, redirects, or approves.

### Step 6: Save the intake brief
Once the owner confirms the proposal, save the evidence brief and confirmed
proposal together to `projects/$ARGUMENTS/intake-brief.md`.

Verify: file exists at the expected path. Read it back and confirm it contains
both the evidence brief and the confirmed proposal direction.

### Step 7: Suggest next step
Tell the owner intake is complete and suggest `/draft-cycle $ARGUMENTS` to
produce the full cycle deliverable.

## If This Fails

- **Research returns no industry-specific results:** Broaden the search — try
  the job function rather than the industry (e.g. "operations manager recurring
  reporting" instead of "manufacturing operations AI"). Flag the gap in the
  evidence brief explicitly.
- **Venture scenario dependency is unresolved and owner wants to proceed
  anyway:** Do not invent a scenario. Present 2–3 scenario options as a
  decision prompt for the owner. Content cannot be written until one is chosen.
- **Owner confirms parameters but they conflict with a non-negotiable:** Name
  the conflict, cite the non-negotiable, and ask before proceeding (see
  Non-Negotiable Conflict Handling in CLAUDE.md).
- **Process type doesn't fit the controlled menu:** Flag it, explain why the
  menu exists (predictable failure engineering), and offer to add it to the
  menu if the owner can confirm the failure mechanic is still engineerable.
- If none of the above resolve it, search online for:
  "[industry] common recurring admin processes AI automation 2025"

After resolving, update `references/lessons-learned.md` with what worked.
