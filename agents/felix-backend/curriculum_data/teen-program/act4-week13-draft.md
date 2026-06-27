# Act 4, Week 13 — FAIL Week
## "What Shape Does It Produce?"
### /draft-cycle — Teen Track, "Build Your AI"

**Status:** FINAL
**Draft date:** 2026-06-27
**Domain (locked):** TikTok/Instagram creator brand — MY/SG
**Act 4 component introduced this week:** Output Format — the fourth and final layer of the student's agent system prompt. Output Format specifies the exact structure, length, and elements of every output the agent produces. Without it, the agent produces different shapes across runs — sometimes a numbered list, sometimes prose, sometimes short, sometimes long — even when content quality is consistent.
**Act 4 failure type surfaced this week:** Format inconsistency — the same agent, the same task, different output structures across runs. Students discover their agent "does it differently every time." The gap: the system prompt tells the agent WHO it is, HOW to work, WHERE to look — but not WHAT SHAPE to produce.
**Intake brief reference:** `projects/teen-program/brief-v3.md` (locked 2026-06-26)
**Dependencies:**
- act3-week12-draft.md (FINAL) — Week 12 scoreboard data required: Act 3 WIN COUNT recorded, all 7-dimension scores, and the Act 4 bridge script planted in Week 12's WIN ceremony. Students arrive knowing Act 4 covers "how to format what it produces."
- Students arrive with their full 3-layer agent: identity card (Act 1) + Workflow (Act 2) + Research section (Act 3). All three confirmed working as of Week 12.

---

## Section 1 — Session Overview

| Field | Value |
|---|---|
| Track | Teen — "Build Your AI" |
| Act | Act 4 — Output Format |
| Week | Week 13 of 16 — FAIL |
| Beat structure | Beat 1: Reconnect + Act 4 intro → Beat 2: FAIL task (run the same 3-post task 3 times, document format variation) → Beat 3: Zara Screen 3 comparison (consistent format across 3 runs), gap naming, Week 14 seed plant |
| Component introduced this week | Output Format. The 8th dimension is added to the scoring instrument this week. Introduced as a gap first — students discover their agent produces inconsistent output shapes before they know how to fix it. |
| Agent in all beats | Student's full 3-layer agent (identity + Workflow + Research section), unchanged from Week 12. No additions in-session. Beat 2 reveals the gap in the current agent. |
| The FAIL principle | FAIL weeks surface the gap by running the current agent. The task in Week 13 is designed so that the gap (format inconsistency) is visible across runs. Content may be fine — the research layer and identity layer are working. The failure is structural: same input, different output shape. |
| Win bar this week | Students can name the FORMAT gap (not a content gap). The specific format element that changed between runs — structure, length, section order, or all three. AND: they can articulate why their current agent cannot guarantee consistency. "It doesn't have instructions for what shape to produce." |
| Comparison this week | Zara Screen 3 — Zara's full 4-layer agent (identity + Workflow + Research + Output Format). Run on the same task 3 times, all 3 outputs have the same structure. The contrast with the student's 3 varied outputs is the gap evidence. |
| Scoring purpose | Week 13 introduces the 8th scoring dimension: Output Format (0–20). Total instrument is now 0–160. Output Format scores 0–5 in Week 13 (not yet built). The 7 established dimensions are also scored; expected stable or slight improvement given the 3-layer agent is well-built. The Output Format gap is introduced as neutral — same as Research Grounding scored 0–5 in Week 9 before being built. |
| Scoring instrument | 8 dimensions. 0–20 each. 0–160 total. First week at 0–160. |
| Facilitator | Human (pilot) |
| Cohort size | 2 students (pilot) |
| Estimated session time | Beat 1: ~6–8 min / Beat 2: ~15–18 min / Beat 3: ~12–15 min / Total: ~33–41 min |
| Persona name | Zara (locked) |
| Temperature | Zara Screen 3: temperature=0. Student agents: default temperature. |

---

## Section 2 — What the Student Brings In

The student enters Week 13 with:

1. **Their identity card from Act 1** — unchanged since Week 2. Three to four sentences specifying niche, audience, voice, and boundaries.
2. **Their Workflow from Act 2** — confirmed in Week 8, unchanged. Step-by-step instructions for how to build a 3-post series arc.
3. **Their Research section from Act 3** — three elements (where to look, what needs verification, uncertainty protocol) plus the recency filter added in Week 11. Verified in Week 12 on two task types.
4. **A planted expectation from Week 12** — the Act 4 bridge: "Act 4 adds the last layer: how to format what it produces." Students know they're building something new. They may not yet know what "format" means as instruction architecture.

**What the student expects:**

Students arrive knowing Act 4 is about format. They may think they already know what "format" means — the visual look of a post (emojis, line breaks, hashtags). Week 13's job is to redirect: format as instruction architecture means specifying the STRUCTURE of each output element (not decoration). The FAIL task reveals this gap through the student's own evidence, not through a definition.

---

**Pre-session check — agent state:**

| Student status | Week 13 path |
|---|---|
| Full 3-layer agent loaded (identity + Workflow + Research with recency filter) | Proceed to Beat 1. |
| Research section missing recency filter (Week 11 async fix not carried forward) | Add recency filter now (~3 min) using the student's Week 11 capture form (d). This is a maintenance fix, not today's build. Do not run the FAIL task until the agent is in Week 12 state. |
| Agent is missing one of the three layers | Stop. Restore the missing layer using prior capture forms before proceeding. Week 13 must run on the complete 3-layer agent — the FAIL task is designed to isolate the Output Format gap, and a missing prior layer would confuse the diagnosis. |

---

## Section 3 — Beat 1 — Reconnect + Act 4 Intro

**Mode:** Facilitator-led. Short. The purpose is to close the Act 3 chapter and name what's coming without explaining it.

**What the facilitator says verbatim to open Week 13:**

*"Three acts down. Your agent has three layers."*

*[Pause.]*

*"Layer one: identity. It knows who it is. Layer two: workflow. It knows how to build a series. Layer three: research. It knows where to get its information and what to do when it can't verify a claim."*

*[Pause.]*

*"Today we run it again — same kind of task, same agent. But we're going to run it THREE times."*

*[Pause.]*

*"Three times. Same prompt. Read the outputs side by side. We're looking for something specific."*

*[Pause.]*

*"You'll see it."*

*[Move directly to Beat 2.]*

---

**Beat 1 timing guide:**

| Segment | Time |
|---|---|
| Act 3 close ("three layers, confirmed") | 1–2 min |
| Act 4 intro framing ("three runs, same prompt") | 1–2 min |
| Agent check + transition | 1–2 min |
| **Total** | **~3–6 min** |

---

## Section 4 — The Output Format Gap (Facilitator Preparation)

*This section is facilitator preparation — not student-facing. Read before Week 13. The FAIL task in Beat 2 is designed to surface format inconsistency naturally. This section explains what the gap looks like, how to recognize it in student outputs, and what the three most common confusions are.*

---

**What Output Format is — and is not:**

Output Format is a set of explicit instructions in the agent's system prompt that specify the STRUCTURE of every output the agent produces. It defines: what each element of the output is, what order it comes in, and how long it should be. Without it, the agent produces correct content in an inconsistent container — the same niche, the same voice, the same research layer, but a different shape every time.

| This IS Output Format | This is NOT Output Format |
|---|---|
| "Every post must follow this structure: HOOK (1 sentence — a question or bold claim, under 15 words) / BODY (3–4 sentences, includes one specific example or local MY/SG reference) / CTA (1 sentence, ends with a direct question to the reader)." | "Make the posts look professional and consistent." |
| "Length: 80–100 words per post. Never exceed 100 words. Never go under 60." | "Keep the posts the right length." |
| "Label each post as Post 1, Post 2, Post 3. Never merge them into a single block of text." | "Format the posts clearly." |

The second column is a style preference, not a structural specification. Style preferences do not constrain the agent's output shape — they produce variation just as if nothing were said. Output Format instructions are specific, measurable, and followable without interpretation.

---

**What format inconsistency looks like across 3 runs:**

The FAIL task asks the student to run a 3-post content task three times. Across runs, format inconsistency may appear as:

| Variation type | What the student sees |
|---|---|
| Structure variation | Run 1: posts have a clear Hook line, a middle section, a closing question. Run 2: posts are flowing prose with no identifiable structure. Run 3: posts open with a fact, have bullet points in the middle, and end with emojis. |
| Length variation | Run 1: posts average 75 words. Run 2: posts average 140 words. Run 3: posts average 50 words. Same topic — dramatically different lengths. |
| Section order variation | Run 1: CTA is the final sentence. Run 2: CTA appears mid-post. Run 3: no clear CTA. |
| Labeling variation | Run 1: outputs are labeled "Post 1 / Post 2 / Post 3." Run 2: outputs are delivered as a flowing narrative with no labels. Run 3: labeled "Post A / Post B / Post C." |

Any single variation type is enough for the FAIL. Multiple variation types are common and make the gap more obvious.

---

**What students get wrong (and how to redirect):**

| Student says | Facilitator redirection |
|---|---|
| "The outputs are different because the AI is random." | "Some variation is AI randomness. But the KIND of variation here — sometimes prose, sometimes bullets, sometimes 50 words, sometimes 150 — is not randomness. It's the agent making formatting decisions on the fly because you haven't told it what shape to produce. That's the gap." |
| "I just need to tell it to 'be consistent.'" | "Try it. Add 'be consistent' to your prompt right now and run it again." [Allow them to run it.] "Did it change?" [It won't reliably.] "That's a preference, not a specification. What you need is a structural spec: HOOK, BODY, CTA — with exact length. That's what Week 14 builds." |
| "The content is good though — why does the shape matter?" | "Your audience sees the shape first. A post with a clear hook in the first sentence reads differently from a post that starts mid-thought. When your agent produces a different shape every time, you spend time reformatting every output before you can use it. An agent with an Output Format spec is deploy-ready — you copy and post. Without it, you copy and edit every time." |
| "Can I just fix the format in the prompt each time I run it?" | "Yes — but that means you're managing the format manually, not your agent. The goal of Act 4 is to move the format decisions INTO the agent's instructions, so you never have to specify it again. One good spec, then every run delivers the same shape." |

---

## Section 5 — Beat 2 — FAIL Task (Three Runs, Same Prompt)

**Trigger:** Beat 1 complete. Student's 3-layer agent is confirmed loaded.

**What the facilitator says before the FAIL task:**

*"You're going to run one task — three times. Exact same prompt, no changes, same agent."*

*[Pause.]*

*"After you have all three outputs: read them side by side. Look at the SHAPE — not the content. Not what the agent said, but HOW it packaged it."*

*[Pause.]*

*"Did the structure change? Did the length change? Did the order of the sections change?"*

*[Pause.]*

*"Write down what you notice. Hit Submit when you have something specific."*

---

**FAIL task card (screen text):**

> **Your task: Run this prompt three times**
>
> Your agent is your full 3-layer agent (identity + Workflow + Research). No changes.
>
> **Prompt to run:**
>
> *"Write a 3-post content series for my [niche] audience about [topic related to their niche — facilitator specifies from student's known niche content]. Each post should work on its own but connect as a series."*
>
> *(Facilitator: fill in the student's specific niche and a topic they've covered before. Keep it familiar — the goal is to isolate format variation, not introduce new content challenges.)*
>
> **Run the prompt once. Save the output (screenshot or copy-paste).**
>
> **Run the same prompt again. Save the output.**
>
> **Run it a third time. Save the output.**
>
> **Now read all three side by side.**
>
> Look at:
> - **Structure** — does each post have the same sections in the same order across all three runs?
> - **Length** — are the posts roughly the same word count across all three runs?
> - **Labels** — are the posts labeled the same way across all three runs?
>
> **Write down the most significant difference you noticed between the three runs.**
>
> Hit **Submit**.

---

**Facilitator notes — Beat 2:**

- **Choose the topic carefully before the session.** Pick a topic in the student's niche that they've already worked on in a prior session. Using a familiar topic isolates the format variable — the student already knows the content is within the agent's capability. A new or challenging topic adds noise.
- **All three runs on the same topic.** The FAIL task must be the same prompt, identical, three times. If a student changes the prompt between runs, the comparison is invalid.
- **Expect mixed results.** Some students will see large format variation (different structures across all three runs). Others will see moderate variation (structure consistent but lengths vary). Rarely: minimal variation. All three cases are useful. Even moderate variation demonstrates the gap — deploy a post series to your audience with 60-word posts AND 150-word posts, and the inconsistency is immediately visible.
- **If the student says "all three look the same to me":** Look at the outputs yourself. Measure word counts. Compare opening sentences — even if the content is similar, the packaging often varies subtly. Find the specific difference and name it: "Post 1 in Run 1 opens with a question. Post 1 in Run 2 opens with a statement. That's a structure variation. One more run — watch that opening sentence."
- **Do not explain Output Format in Beat 2.** The FAIL task's job is to produce evidence of the gap, not to diagnose it. The diagnosis comes in Beat 3 with the Zara comparison.

---

**Beat 2 timing guide:**

| Segment | Time |
|---|---|
| Facilitator frames the FAIL task | 1–2 min |
| Students run the prompt three times + save outputs | 8–10 min |
| Students compare outputs and write their observation | 2–3 min |
| Transition to Beat 3 | 30 sec |
| **Total** | **~12–16 min** |

---

## Section 6 — Zara Screen 3 Comparison + Gap Naming

**Trigger:** Beat 2 complete. Students have observed format variation in their 3 runs.

**What the facilitator says before showing Zara:**

*"What did you notice?"*

*[Receive: student names the format variation — structure, length, or section order.]*

*[Pause.]*

*"Good. Now look at Zara."*

*[Display Zara Screen 3 — all three runs of Zara's full 4-layer agent on the same task, side by side.]*

---

**Facilitator preparation — Zara Screen 3:**

Before Week 13, run Zara's full agent (Screen 3 — identity + Workflow + Research Grounding + Output Format section) at temperature=0 on the same FAIL task three times. Zara's Output Format section specifies:

- Every post: HOOK (1 sentence, question or bold claim, under 15 words) / BODY (3–4 sentences, one specific example) / CTA (1 sentence, direct question to reader).
- Length: 80–100 words per post.
- Label each post: **Post 1 / Post 2 / Post 3**.

All three of Zara's runs should produce the same structure. The comparison is visual — show all three Zara runs and all three student runs simultaneously if possible, or sequentially.

---

**What the facilitator says after showing Zara's output:**

*"Find the structure of Zara's first post across all three runs. Is it the same?"*

*[Students read. They confirm: same structure, same length range, same labels.]*

*"What's different about your three runs?"*

*[Students name the difference.]*

*"Here's the question: what did you tell your agent about what shape to produce?"*

*[Pause. Students realize: nothing.]*

*"Your agent knows WHO it is. It knows HOW to work. It knows WHERE to look. But you never told it WHAT SHAPE to produce. So it decides on the fly — and it decides differently every time. That's not a content problem. That's an architecture problem."*

*[Pause.]*

*"Zara's agent has a fourth section. It doesn't just tell her agent WHAT to write — it tells it HOW to package what it writes. Every time, the same container."*

*[Pause.]*

*"Week 14: you build that section."*

---

**The Week 14 seed — facilitator script (verbatim):**

*"Your agent knows WHO it is, HOW to work, WHERE to look. But it doesn't know WHAT SHAPE to produce. Week 14 fixes that."*

*[Pause.]*

*"Before Week 14: look through your previous outputs from this program — or your actual social media posts if you have them. Find the one post you're most proud of, or the one that performed best. We're going to use that as the template for your Output Format spec."*

*[Pause.]*

*"That's the homework. One post — your best one. Bring it to Week 14."*

---

**Beat 3 timing guide:**

| Segment | Time |
|---|---|
| Student names their format variation | 1–2 min |
| Zara Screen 3 shown | 2–3 min |
| Facilitator names the gap ("not what shape to produce") | 2–3 min |
| Week 14 seed + pre-Week 14 homework | 2–3 min |
| Individual notes / questions | 1–2 min |
| **Total** | **~8–13 min** |

---

## Section 7 — Student Reaction Handling

**The emotional register of Beat 3 is curious and slightly surprised — this is a gap students have been living with but hadn't named.** They've been using their agent and probably reformatting outputs manually. Week 13 names that invisible friction.

---

**Reaction A — "I didn't notice the format changing before."**

*What the facilitator says:*

*"Most people don't — because they're reading for content. The format variation is only obvious when you're looking for it, or when you try to publish three posts from different runs side by side. When you do that, the inconsistency is immediately visible. That's what the audience sees — not the words, but the shape."*

---

**Reaction B — "My runs actually looked similar — I'm not sure the format changed much."**

*What the facilitator says:*

*"Let's check the lengths."*

*[Measure word counts for the three sets of posts. Even similar-looking outputs often vary 30–50% in word count between runs.]*

*[If lengths are truly similar:] "Your agent may have developed consistent format tendencies from a well-built Workflow. That's good news — it means the gap may be smaller for you. The STRETCH in Week 15 will confirm whether the format holds under different task conditions. The build in Week 14 will lock it in explicitly so it holds by instruction, not by habit."*

---

**Reaction C — "Can I just add 'output it the same way every time' to my prompt?"**

*What the facilitator says:*

*"Try it right now. Add that instruction and run it twice."*

*[Allow a quick live test — the instruction will likely produce minimal or no change.]*

*"That's a preference, not a specification. The agent doesn't know what 'the same way' means until you tell it exactly what the structure is. Week 14 is the session where you define that structure precisely — not as a preference but as a spec."*

---

**Reaction D — "Does the format matter that much for a social post?"**

*What the facilitator says:*

*"Here's the test: when you used your agent in the last twelve weeks, how much did you edit the outputs before they were ready to post or share? Every time you reformatted, restructured, or resized a post — that was you doing work your agent should have done. An agent with an Output Format spec gives you deploy-ready output — the shape you asked for, every time, without reformatting. That time you saved? That's what the Output Format layer buys."*

---

## Section 8 — Scoring Instrument — Week 13

**New this week: 8th dimension — Output Format (0–20). Total instrument: 0–160.**

The Output Format dimension is introduced this week alongside the gap discovery. Students will score 0–5 on this dimension in Week 13 because the Output Format layer is not yet built. This is not failure — it is the same baseline condition as Research Grounding in Week 9 (0–5 before the Research section was built).

**Output Format scoring rubric (for facilitator reference):**

| Score range | What it means |
|---|---|
| 0–5 | Output Format layer not present. Output structure varies significantly across runs. No explicit format specification in system prompt. |
| 6–10 | Partial format guidance present — some structural direction but not explicit or measurable. E.g., student has mentioned "post should have a hook" but no length or order spec. |
| 11–15 | Output Format section present with named elements and order. Some but not all length guidance specified. Structure is mostly consistent across runs. |
| 16–20 | Output Format section present with named elements, order, and length guidance for all elements. Outputs are structurally consistent across 3 runs. |

**When to score:** Facilitator scores after the session using the Beat 2 FAIL task outputs (all 3 runs).

**Expected score movement (Week 13):**

| Dimension | Week 13 expected | Note |
|---|---|---|
| Consistency | Stable (15–20) | Identity card unchanged |
| Specificity | Stable (15–20) | Identity card unchanged |
| Local grounding | Stable | Unchanged |
| Questioning behavior | Stable | Unchanged |
| Claim integrity | Stable | Research section unchanged |
| Series coherence | Stable | Workflow unchanged |
| Research Grounding | Stable (15–18) | Research section confirmed Week 12 |
| **Output Format** | **0–5** | Not yet built. Expected baseline. |
| **TOTAL** | **~100–120/160** | Seven built dimensions stable; Output Format at baseline. |

---

## Section 9 — Facilitator Capture Form

*Per student, per session. Captured after Beat 3 closes.*

| # | What to capture | Format | Why it matters |
|---|---|---|---|
| (a) | **The FAIL task prompt used** — the specific niche topic and prompt text run three times. | Full prompt text | Required for Week 16 regression check. Beat 1 of Week 16 repeats this exact prompt. |
| (b) | **The format variation observed.** What specifically changed across the three runs — structure, length, section order, labeling. The most significant difference the student named. | Type of variation + one sentence description | Primary evidence of the Output Format gap. Use in Week 14 opening to anchor the build. |
| (c) | **Zara comparison landing.** Did the student see the structural consistency in Zara's 3 runs? What was the contrast they named? | Yes/No + what they named | Confirms the gap diagnosis landed correctly. |
| (d) | **Pre-Week 14 homework confirmation.** Did the student identify a "best post" to bring to Week 14? From program outputs or from their own social media? | Yes/No + source (program or own) | Week 14 Beat 2 starts from this post. If the student hasn't done this homework, facilitator needs a quick in-session extraction at Beat 2 open. |
| (e) | **Week 13 scores — all 8 dimensions.** | 8 scores | First record at the 0–160 instrument. Archive for Act 4 WIN ceremony (Week 16 scoreboard). |

**Minimum viable capture:** (a) and (b). The FAIL task prompt (needed for Week 16 regression) and the format variation observed (the gap evidence to anchor Week 14).

---

## Section 10 — Structural Notes

**The FAIL task must isolate format as the variable.** The task in Beat 2 runs the same prompt on the same agent three times. The topic must be familiar and within the agent's capability — introducing a new or challenging topic would add content-quality noise that obscures the format gap. If a student's outputs also show content quality issues across the three runs, diagnose those separately and note whether they trace to the format gap or to an existing layer issue (usually Research section precision).

**Output Format is NOT about visual decoration.** The most common early misconception is that "format" means emojis, line spacing, hashtag placement, or visual style. Redirect immediately: Output Format as instruction architecture means structural specification — named elements, order, length. Visual style choices are handled inside the elements (e.g., "HOOK — one sentence, conversational, no hashtags in the hook line"). Do not let students conflate the two in Week 13.

**8th dimension introduction is neutral — not a failure moment.** When introducing the Output Format dimension on the scoring instrument, frame it the same way Research Grounding was framed in Week 9: "You haven't built this yet, so it scores at zero. By Week 16, it will score. That's what Act 4 does." The low Output Format score in Week 13 should not feel like a setback — it should feel like a known starting point.

**Do not preview the Output Format BUILD.** Students may ask in Beat 3 how to build the Output Format section. The Week 14 seed ("find your best post") is the pre-work, not a preview of the build method. Redirect: "Week 14 is the build session. Bring your best post and you'll see how it becomes the template."

---

## Section 11 — Week 13 Summary

**What happened this week:**

Students arrived with their full 3-layer agent from Act 3. Beat 1 closed Act 3 quickly and named what Act 4 is about. Beat 2 ran the same 3-post content task three times and asked students to compare outputs for format variation. The evidence was their own — across three identical runs, the agent produced different structures, different lengths, different section orders, or some combination. The gap was visible before it was explained.

Beat 3 showed Zara Screen 3: the same task, three runs, the same structure every time — because her Output Format section specifies exactly what shape every output must take. The contrast with the student's varied outputs named the gap: the agent knows WHO it is, HOW to work, WHERE to look — but not WHAT SHAPE to produce.

The 8th scoring dimension was introduced. Output Format scores 0–5 this week — the baseline before the build. The pre-Week 14 homework was planted: find the one post you're most proud of.

**What the student now has:**

1. **A named gap.** Format inconsistency — the agent produces different structures across runs. The student has their own evidence from three runs.
2. **The gap articulation.** "My agent doesn't know what shape to produce."
3. **A pre-Week 14 task.** One best post — from the program or from their own portfolio — to bring to Week 14 as the template for the Output Format spec.

**Bridge sentence to Week 14 — facilitator close:**

*"Your agent doesn't have a format spec. Week 14: you're going to write one — starting from the best output you've already produced."*

---

## Section 13 — Director Approval

Director Approval — Clean Approval. No arbitration items. All design decisions approved as drafted.

---

*End of Act 4, Week 13 — FINAL*
