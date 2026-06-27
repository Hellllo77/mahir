# Act 4, Week 14 — FIX/BUILD Week
## "The Format Layer"
### /draft-cycle — Teen Track, "Build Your AI"

**Status:** FINAL
**Draft date:** 2026-06-27
**Domain (locked):** TikTok/Instagram creator brand — MY/SG
**Act 4 component built this week:** Output Format — a dedicated Output Format section added to the system prompt. Contains: (1) named structural elements with labels (e.g., HOOK / BODY / CTA or equivalent for the student's niche), (2) order of those elements, (3) explicit length guidance for each element. The source for the spec: the student's own best post, reverse-engineered into a replicable template.
**Act 4 failure type fixed this week:** Format inconsistency established in Week 13. The agent produced different structures across identical runs. This week gives it an explicit format spec derived from the student's own best work.
**Intake brief reference:** `projects/teen-program/brief-v3.md` (locked 2026-06-26)
**Dependencies:**
- act4-week13-draft.md (DRAFT) — Week 13 Section 9 capture data required: the specific format variation the student observed (type: structure / length / section order / labeling), and confirmation of the pre-Week 14 homework (best post identified).
- Pre-Week 14: students were asked to find their best post (from program outputs or their own social media). This post is the anchor for the Output Format spec they write in Beat 2.
- All Act 4 Week 13 scores (8 dimensions) — archived per Section 9 capture. Output Format Week 13 baseline score recorded.

---

## Section 1 — Session Overview

| Field | Value |
|---|---|
| Track | Teen — "Build Your AI" |
| Act | Act 4 — Output Format |
| Week | Week 14 of 16 — FIX/BUILD |
| Beat structure | Beat 1: Reconnect + Week 13 gap recap → Beat 2: BUILD — reverse-engineer the best post, write the Output Format section (three required elements) → Beat 3: Consistency check (run the Week 13 task 3 times with Output Format built in, compare structure across runs) |
| Component built this week | Output Format. Students add an Output Format section to their system prompt. The section is derived from their own best post — not from an arbitrary template. Three required elements: named structural components, their order, and explicit length guidance. |
| Agent in all beats | Student's identity card + Workflow + Research section (unchanged). The Output Format section is the only new addition, written and loaded in Beat 2. Beat 3 runs with the complete 4-layer agent. |
| The BUILD principle | FIX/BUILD weeks build one thing deliberately and verify the fix holds on the same task that exposed the gap. The build in Week 14 is architectural: a new section in the system prompt, not a revision to existing sections. The identity card, Workflow, and Research section are untouched. |
| Win bar this week | The student's 4-layer agent runs the Week 13 task 3 times and produces the same structure each time — named elements in the same order, lengths within the specified range. The Output Format section is the evidence of the build; the consistency check is the evidence it works. |
| Comparison this week | None in-session — the comparison is the student's own 3 new runs against their Week 13 varied runs. The contrast is internal: same agent, same task, same 3 runs — but now with the Output Format section present. |
| Scoring purpose | Week 14 is the first live score for Output Format with the layer present. Expected movement: 0–5 (Week 13) → 12–18 (Week 14). The build is new; the Output Format section may not yet cover all edge cases — that is expected. Week 15 (STRETCH) stress-tests the spec under different output contexts. |
| Scoring instrument | 8 dimensions × 20 = 0–160 total. |
| Facilitator | Human (pilot) |
| Cohort size | 2 students (pilot) |
| Estimated session time | Beat 1: ~5–7 min / Beat 2: ~18–22 min / Beat 3: ~12–15 min / Total: ~35–44 min |
| Persona name | Zara (locked — not used in Week 14) |
| Temperature | Student agents: default temperature. |

---

## Section 2 — What the Student Brings In

The student enters Week 14 with:

1. **Their identity card from Act 1** — unchanged since Week 2.
2. **Their Workflow from Act 2** — confirmed in Week 8, unchanged since.
3. **Their Research section from Act 3** — three elements plus recency filter. Confirmed in Week 12.
4. **A named gap from Week 13** — the student knows their agent produces inconsistent output shapes across runs. They know the specific variation type they observed. They know why: the system prompt has no Output Format specification.
5. **A best post** — the pre-Week 14 homework. The student identified one post they're most proud of (from program outputs or their own social media). This is the template for the Output Format spec.

**What the student expects:**

Students arrive ready to write something — Week 13 planted the task clearly: "find your best post and bring it to Week 14." Students who completed the homework are ready to reverse-engineer their post's structure immediately in Beat 2. Students who did not identify a post need a 3-minute facilitator-led extraction before Beat 2 can open.

The session's job is to make the Output Format spec feel DERIVED, not invented. The student is not guessing at a format — they are formalizing the format that already produced their best result.

---

**Pre-session check — Week 13 best post:**

| Student status | Week 14 path |
|---|---|
| Has a specific best post ready (from homework) | Open Beat 2 with the post as the anchor. Proceed to reverse-engineering. |
| Cannot recall or did not identify a best post | 3-minute extraction: "Look through your saves from this program. Which output did you like most — or would you actually post?" Use the Week 13 capture form outputs as candidates if the student's own portfolio is unavailable. |
| Has multiple posts and can't choose | "Pick the one you'd post right now without editing. That's the one." Speed-decision — don't allow comparison paralysis. |

---

## Section 3 — Beat 1 — Reconnect + Week 13 Gap Recap

**Mode:** Facilitator-led. Short. Beat 1 closes Week 13's chapter and anchors the build in the gap evidence.

**What the facilitator says verbatim to open Week 14:**

*"Week 13. You ran the same task three times."*

*[Pause.]*

*"What changed between the runs?"*

*[Receive: the student names the format variation — structure, length, section order. Use the Week 13 capture form (b) to confirm.]*

*[Pause.]*

*"Right. Same agent. Same prompt. Different shape. Not a content problem — an architecture problem. Your agent had no instructions for what to produce."*

*[Pause.]*

*"Today you fix that. Not by telling it to be consistent — by giving it an explicit spec. And we're going to build the spec from your best post."*

*[Pause.]*

*"Did you bring it?"*

*[Receive: student confirms the post. Move directly to Beat 2.]*

---

**Beat 1 timing guide:**

| Segment | Time |
|---|---|
| Week 13 gap recap (name the specific variation) | 2–3 min |
| Framing the fix ("spec from your best post, not invented") | 1–2 min |
| Best post confirmation + transition | 30 sec |
| **Total** | **~4–6 min** |

---

## Section 4 — The Output Format Build (Facilitator Preparation)

*This section is facilitator preparation — not student-facing. Read before Week 14. The BUILD in Beat 2 requires the facilitator to guide students toward a spec that is EXPLICIT, LABELED, and LENGTH-SPECIFIC. The most common error is allowing students to write preferences instead of specifications. This section equips the facilitator to catch and redirect.*

---

**What an Output Format section contains — three required elements:**

**Element 1 — Named structural components with labels:**
- What it is: explicit labels for each part of the output, not just a description of what goes there. Labels are specific enough that the agent can identify where each element starts and ends.
- Example: "HOOK — the opening sentence. BODY — the middle 3–4 sentences. CTA — the closing sentence."
- Common failure: "Start with something attention-grabbing, then explain the topic, then end with something." This describes the function but doesn't label the parts. Without labels, the agent can't be instructed to keep each element to a specific length or order.

**Element 2 — Order of components:**
- What it is: the explicit sequence in which the labeled elements appear. Not assumed — stated.
- Example: "Every post must follow this order: HOOK → BODY → CTA. No exceptions."
- Common failure: naming the components without specifying the order, then getting surprised when the agent sometimes puts the CTA first or weaves it into the body.

**Element 3 — Length guidance for each element:**
- What it is: explicit word count, sentence count, or character count for each named element. Must be specific enough to distinguish a 15-word hook from a 60-word hook.
- Example: "HOOK: 1 sentence, maximum 15 words. BODY: 3–4 sentences, maximum 80 words total. CTA: 1 sentence, ends with a question."
- Common failure: "Keep it concise" or "around 100 words" — these are preferences. A 100-word target without element-level guidance still produces posts where the hook is 2 sentences and the body is 1.

---

**The reverse-engineering process — how to run Beat 2:**

The BUILD in Week 14 is distinct from the BUILD in Weeks 6 and 10 because the spec is derived from the student's own best post. The facilitator's role is to ask the right questions, not to prescribe the format.

Step 1 — Read the best post aloud: the facilitator reads the student's best post aloud (or the student reads it). This gives the post critical distance — hearing it rather than just seeing it makes the structure more obvious.

Step 2 — Ask: "What does the first sentence do?" The answer should be something like "it grabs attention" or "it asks a question" or "it states a bold fact." That function is the HOOK. Label it.

Step 3 — Ask: "What do the middle sentences do?" The answer should identify the supporting content. That's the BODY. How many sentences? What's in there — example, explanation, local reference?

Step 4 — Ask: "What does the last sentence do?" The answer is typically "it invites the reader to do something" or "it asks them a question." That's the CTA. Label it.

Step 5 — Measure: count the words in each element. Set the length guidance from what's actually in the best post. Students should write what they measured, not what sounds good.

Step 6 — Write the spec: convert the answers into explicit Output Format instructions. Label, order, length. Load into the system prompt as a new section.

---

**What an Output Format section looks like (example for a MY/SG creator niche):**

> **Output Format:**
>
> Every post must follow this structure in this order:
>
> **HOOK** — The first sentence only. A bold claim or direct question to the reader. Maximum 15 words. No hashtags in the hook.
>
> **BODY** — 3 sentences. One of the three sentences must include a specific example, local reference, or real number. Total body: 50–80 words.
>
> **CTA** — The final sentence only. A direct question inviting the reader to respond, share, or try something. Maximum 20 words.
>
> **Post length:** 70–100 words per post.
>
> **Labeling:** Output each post as "**Post 1:**", "**Post 2:**", "**Post 3:**" — bold, on its own line, before the post content.

*This example is illustrative. The student's spec will differ based on their niche, their best post's structure, and the element names that fit their content type.*

---

**Element naming for different creator niches:**

Students should label their elements in terms that fit their niche. HOOK / BODY / CTA is one system — not the only one. For different niches:

| Niche type | Possible element names |
|---|---|
| Finance / education | INSIGHT (opening claim) / EXPLANATION (why it works) / TAKEAWAY (what the reader does next) |
| Fitness / wellness | CHALLENGE (the problem or question) / APPROACH (what works and why) / PROMPT (what to try today) |
| Food / lifestyle | HOOK (attention line) / STORY (the context or detail) / INVITE (what to do or try) |
| Gaming / tech | SETUP (the situation or problem) / BREAKDOWN (the analysis) / VERDICT (the conclusion or recommendation) |

The specific labels don't matter — the principle is that each element is NAMED, ORDERED, and LENGTH-SPECIFIED.

---

## Section 5 — Beat 2 — Writing the Output Format Section

**Trigger:** Beat 1 complete. Student has their best post in front of them.

**What the facilitator says before the build:**

*"Read your post. Not for the content — for the structure."*

*[Pause.]*

*"First sentence. What does it do? What's its job?"*

*[Receive: student names the function. Help them label it.]*

*"Middle section. What does it do? How many sentences?"*

*[Receive: student names the function. Count sentences together.]*

*"Last sentence. What does it do?"*

*[Receive: student names the function. Help them label it.]*

*"Now count the words. How long is the hook? How long is the middle? Total length of the post?"*

*[Receive: student counts. Note the numbers.]*

*"Good. Now you write a spec that would make an agent produce this structure every time — starting from scratch, with no post to reference. Named elements. Order. Length. Specific enough that your agent could follow it without asking you what you mean."*

---

**Build card (student-facing — on screen):**

> **Your task: Build your Output Format section**
>
> Open your agent's system prompt. Add a new section after your Research section. Label it: **Output Format**.
>
> **Your Output Format section must include all three of the following:**
>
> **1. Named structural elements**
> Label each part of your post with a name. Look at your best post — what does the first part do? What does the middle do? What does the end do? Give each part a label (HOOK / BODY / CTA or your own names for your niche).
>
> *Example: "HOOK — the opening. CHALLENGE — the middle content. TAKEAWAY — the close."*
>
> **2. The order of elements**
> State the exact sequence your agent must follow every time. No assumptions.
>
> *Example: "Every post must follow this order: HOOK → CHALLENGE → TAKEAWAY. This sequence is non-negotiable."*
>
> **3. Length guidance for each element**
> Specify how long each element should be — in words, sentences, or characters. Base this on your best post: count the words in each element. Use those numbers.
>
> *Example: "HOOK: 1 sentence, max 15 words. CHALLENGE: 3 sentences, 50–70 words total. TAKEAWAY: 1 sentence, ends with a question, max 20 words."*
>
> **When you're done:** read your Output Format section out loud. Ask: could an agent produce my best post's structure by following these instructions alone — with no other guidance and no example post? If yes, you're done. If not, add one more specific detail.
>
> Hit **Submit** when your Output Format section is complete.

---

**Facilitator notes — Beat 2:**

- **The facilitator's role is to push for specificity — not to prescribe the spec.** The student's Output Format should emerge from THEIR best post, not from the example in the build card. Circulate and ask: "Is that specific enough? What does '3–4 sentences' mean — are you specifying that as a hard rule or a suggestion?"
- **Common failure: writing a description of the format instead of instructions for it.** "The hook should be engaging" describes what good looks like — it doesn't specify what the agent should do. Push to the instruction: "The hook is one sentence, begins with a question or bold claim, under 15 words." That is followable without interpretation.
- **Length guidance is the most commonly weak element.** Students write "keep it short" or "around 100 words." These are preferences. Push to numbers: "How short? 80 words? 60 words? Your best post was [X] words — use that." Exact numbers are better than ranges. If a student genuinely isn't sure, use a ±20-word range: "80–100 words total."
- **The "could an agent follow it" self-check is the key test.** Before the student submits, have them read the Output Format section aloud and ask: "Could your agent follow these exact instructions — without seeing your best post — and produce the same structure?" If yes, it's specific enough. If they hesitate, that's where the spec needs more precision.
- **No changes to other sections in Beat 2.** If a student wants to update their Workflow or Research section based on what they're noticing: redirect to the next available session. Beat 2 is the Output Format build only.

---

**Beat 2 timing guide:**

| Segment | Time |
|---|---|
| Facilitator reads best post with student + extracts element names | 4–5 min |
| Student measures element lengths (word count) | 1–2 min |
| Student writes Element 1 (named components) | 3–4 min |
| Student writes Element 2 (order) | 1–2 min |
| Student writes Element 3 (length guidance) | 3–4 min |
| Self-check + submission | 1–2 min |
| **Total** | **~13–19 min** |

---

## Section 6 — Beat 3 — Consistency Check (Three Runs)

**Trigger:** Beat 2 complete. Student has submitted an Output Format section with all three elements.

**What the facilitator says before the consistency check:**

*"Same task as Week 13. Exact same prompt. Same agent — now with the Output Format section."*

*[Pause.]*

*"Run it three times. Same as last week. What we're looking for: is the structure the same across all three runs? Same elements? Same order? Similar length?"*

*[Pause.]*

*"Run it."*

---

**Beat 3 task card (exact screen text):**

> **Your task: Run the consistency check**
>
> Your agent now has your Output Format section. Load the updated 4-layer system prompt.
>
> **Run the same Week 13 task prompt three times.** (Facilitator confirms the exact prompt — from Week 13 Section 9 capture (a).)
>
> **After all three runs:**
>
> **Step 1.** Compare the structure of Post 1 across all three runs. Is the opening sentence type the same (question, bold claim, fact)? Is it roughly the same length?
>
> **Step 2.** Compare the total post length across all three runs. Are they within a similar word-count range?
>
> **Step 3.** Compare the closing element (CTA or equivalent). Same function? Same position?
>
> **Step 4.** Note: did the structure hold across all three runs, or did one run break the format?
>
> Hit **Submit**.

---

**Facilitator notes — Beat 3:**

- **The ideal Beat 3 result:** all three runs produce the same labeled elements in the same order within the specified length range. Even if the content differs between runs, the container is the same. This is Output Format working.
- **If one run breaks the format:** compare that run's output against the Output Format spec. Usually the break traces to an underspecified element — "concise" instead of "max 80 words," or "ends with a question" without specifying that it's the ONLY closing sentence. Note the specific failure for Section 9 capture. A single-run break doesn't invalidate the build — it identifies the next precision point.
- **If all three runs still vary significantly:** the Output Format section may be using preference language instead of structural language. Review the student's spec: is every element labeled, ordered, and length-specified? If not, this is a Beat 2 completion issue — allow a focused revision to the underspecified element, then run once more.
- **The "Week 13 vs Week 14" comparison is the teaching moment.** After students submit their Beat 3 result, ask: "Compare those three runs to your three runs from Week 13. What's different?" The student's own evidence — before and after — is more convincing than any facilitator explanation.

---

**The Week 15 seed — facilitator script (verbatim):**

*"Your Output Format section is built. Week 15: we're going to stress-test it on a harder condition — a task where your format needs to flex. One short output, one long output. Same agent, different contexts."*

*[Pause.]*

*"Think about this: your current Output Format spec is built for one format — your standard post. What if someone asked for a TikTok caption — under 150 characters total? Or a blog intro — 300 to 400 words? Does your current spec handle those?"*

*[Pause.]*

*"That's Week 15. Bring your current Output Format spec as-is — don't change it before then. The STRETCH is designed to find the boundary."*

---

**Beat 3 timing guide:**

| Segment | Time |
|---|---|
| Facilitator frames the consistency check | 1–2 min |
| Students load updated agent + run task three times | 6–8 min |
| Students compare three outputs against their spec | 2–3 min |
| Week 13 vs Week 14 comparison moment | 1–2 min |
| Week 15 seed plant | 1–2 min |
| **Total** | **~11–17 min** |

---

## Section 7 — Student Reaction Handling

**The emotional register of Beat 3 is constructive and satisfying** — this is one of the most mechanically visible builds in the program. The student can literally see the structure lock in across three runs in a way that wasn't there in Week 13.

---

**Reaction A — "The structure is the same across all three! This is the most obvious change so far."**

*What the facilitator says:*

*"That's the Output Format layer working. The content is still being generated freshly each run — but the container is fixed. Your agent knows exactly what shape to produce because you told it explicitly. That's what fourteen weeks of instruction architecture looks like in action."*

---

**Reaction B — "One of my runs broke the format. The third one went off-structure."**

*What the facilitator says:*

*"Look at your Output Format spec — specifically the element that broke. What did your spec say about that element? Read it out loud."*

*[Student reads the relevant spec element. Often it's an under-specified length or a missing order constraint.]*

*"There's your gap. 'Around 100 words' is a suggestion — your agent picked a different interpretation on that run. Change it to a specific number — '90–100 words' — and run it once more. One targeted fix."*

---

**Reaction C — "My format is consistent, but the posts feel a bit formulaic now."**

*What the facilitator says:*

*"That's real. A tight Output Format spec produces consistency — and with consistency can come repetitiveness. There are two ways to address that: (a) widen the length range slightly so there's natural variation in how the agent fills the structure; (b) add an instruction within the BODY element: 'one sentence in the body must be different in type — a question, a list item, or a quoted observation — in each post.' That introduces variation inside the structure. We can tune that after Week 15 if it's still feeling rigid — don't change the spec before the STRETCH."*

---

**Reaction D — "I want to build Output Format specs for different content types — not just posts."**

*What the facilitator says:*

*"That's exactly what Week 15 is. Your current spec is for one output context — your standard post. The STRETCH is designed to find out whether your spec is flexible enough to handle different contexts. Don't get ahead of it — bring your current spec to Week 15 as-is and let the task reveal the gap."*

---

## Section 8 — Scoring Instrument — Week 14

**When to score:** Facilitator scores after the session using the Beat 3 consistency check outputs (all 3 runs).

**Expected score movement (Week 14 vs Week 13):**

| Dimension | Expected movement | Driver |
|---|---|---|
| Consistency | Stable | Identity card unchanged |
| Specificity | Stable | Identity card unchanged |
| Local grounding | Stable | Unchanged |
| Questioning behavior | Stable | Unchanged |
| Claim integrity | Stable | Research section unchanged |
| Series coherence | Stable | Workflow unchanged |
| Research Grounding | Stable (15–18) | Research section unchanged |
| **Output Format** | **+10 to +15 (from 0–5 to 12–18)** | Output Format section added — all three elements present, consistency check run, structure holds across 3 runs. May not yet cover all output contexts — that is the STRETCH's job. |

**Output Format scoring note for Week 14:** Score by checking the Beat 3 consistency check outputs. Sub-component (a) Structural Specification — does the Output Format section contain named elements, explicit order, and length guidance? Sub-component (b) Structural Adherence — did all three runs produce the specified structure within the length range? Score 12–14 if structure held on 2 of 3 runs or if one element's length guidance was loose. Score 15–18 if all three runs held to spec with no structural breaks.

---

## Section 9 — Facilitator Capture Form

*Per student, per session. Captured after Beat 3 closes.*

| # | What to capture | Format | Why it matters |
|---|---|---|---|
| (a) | **Output Format section verbatim.** All three elements: named components, order, length guidance. | Full text | The Output Format section is the core artifact of Week 14. Archive for Week 16 graduation (student reads this as part of the full system prompt). |
| (b) | **Best post used as template.** Which post did the student use? What were the element names they extracted? | Post description + element names | Confirms the spec is grounded in the student's actual best work, not invented. Useful for Week 15 STRETCH debrief. |
| (c) | **Consistency check result.** Did all three Week 14 runs produce the same structure? Any run that broke — which element, and was it a spec precision issue? | CONSISTENT / PARTIAL / BROKE + element name if PARTIAL or BROKE | Primary evidence that the Output Format build works. If BROKE, note the fix needed. |
| (d) | **Week 15 seed landing.** Did the student understand the conditional format challenge — that the current spec may not handle different output contexts? | Understood / Unclear + one sentence | Calibrates Week 15 opening. A student who's already thinking about multi-format needs a different opening than one who thinks the STRETCH will be easy. |
| (e) | **Week 14 scores — all 8 dimensions.** | 8 scores | First Output Format score with layer present. Archive for WIN ceremony. |

**Minimum viable capture:** (a) and (c). The Output Format section text and the consistency check result.

---

## Section 10 — Structural Notes

**The build is mechanical — do not let mechanical mean hollow.** Sage's practitioner input flags this explicitly: the risk of the Output Format build is that students feel like they're "just filling in blanks." The teaching job in Week 14 is to connect the spec back to WHY format matters: the audience recognizes a creator's post by its structure before they read the words. A consistent format is part of the creator's brand. The spec they're writing is not a template — it's a signature.

**Three elements are required — do not accept an Output Format section missing Element 3.** Length guidance is the most commonly omitted and the most consequential. Without it, the agent will produce the right elements in the right order — but at wildly different lengths between runs. "Under 100 words" is better than nothing; "80–100 words total for the post" is required. Enforce all three before a student submits for Beat 3.

**Week 15 previews the conditional format gap — do not hint at it now.** The rigidity failure (where the Output Format spec is too rigid for a different output context) is the STRETCH task's discovery. Do not pre-explain conditional formatting in Week 14. Let the student's spec go into Week 15 exactly as written — the STRETCH is designed to surface the next gap naturally. Instructing students not to change their spec before Week 15 is important.

**The best post anchor is the differentiator.** The Output Format spec built in Week 14 is grounded in the student's own best work — not in an external template or arbitrary structure. This makes the spec personally meaningful AND more likely to produce output the student actually wants. If a student doesn't have a "best post" to reference, use the Week 13 outputs: "Which run's Post 1 did you like most? That's your template."

---

## Section 11 — Week 14 Summary

**What happened this week:**

Students arrived with their best post and a named gap from Week 13. Beat 1 closed the Week 13 chapter quickly — the gap was already named; today's job was to build the fix. Beat 2 reverse-engineered the best post's structure: named elements, order, length. The Output Format section was written from what the student already produced, not from an invented template. Beat 3 ran the same three-run consistency check from Week 13 with the updated agent. The verification output was compared across three runs — did the structure hold?

**What the student now has:**

1. **An Output Format section.** Three elements: named structural components, their order, and explicit length guidance. Derived from the student's own best post — a spec they understand because they built it from their own best work.
2. **A consistency confirmation.** Three runs of the Week 13 task with the updated agent. The structure should have held across all three — or a specific precision gap was identified for a targeted fix.
3. **A Week 15 seed.** The conditional format challenge: short-form and long-form output contexts. The current spec may not handle both. The student knows not to change their spec before Week 15.

**Bridge sentence to Week 15 — facilitator close:**

*"Your Output Format spec works for your standard post. Week 15: we find out whether it works when the context changes — short-form and long-form. Different containers. Same agent."*

---

## Section 13 — Director Approval

Director Approval — Clean Approval. No arbitration items. All design decisions approved as drafted.

---

*End of Act 4, Week 14 — FINAL*
