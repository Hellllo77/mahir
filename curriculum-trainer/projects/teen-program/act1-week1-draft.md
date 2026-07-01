# Act 1, Week 1 — FAIL Week
## "The Lottery"
### /draft-cycle — Teen Track, "Build Your AI"

**Draft date:** 2026-06-26
**Domain (locked):** TikTok/Instagram creator brand — MY/SG
**Act 1 failure type:** Randomness (primary) + Hallucination shock (planted only)
**Act 1 component:** Persona / Scope — what the agent IS and what it refuses
**Intake brief reference:** `projects/teen-act1-week1/intake-brief.md` (domain updated: food brand superseded by creator brand per brief-v3.md, locked 2026-06-26)

---

## Section 1 — Cycle Metadata

| Field | Value |
|---|---|
| Track | Teen — "Build Your AI" |
| Act | Act 1 — Persona / Scope |
| Week | Week 1 of 16 — FAIL |
| Failure type | Randomness (primary) / Hallucination shock (secondary, planted only — full arc Act 2) |
| Beat structure | Beat 1: Screen 2 only → Beat 2: Screen 1 revealed → Beat 3: Gap named + seed planted |
| Component built this week | None — failure felt only; build begins Week 2 |
| Facilitator | Human (pilot) |
| Cohort size | 4–8 students |
| Estimated session time | Beat 1: 15–20 min / Beat 2 + 3: 8–10 min / Total: ~25–30 min |
| Screen 2 prompt | Pre-scripted (students copy exact wording — required for consistent failure and comparable baseline scores) |

---

## Section 2 — Scenario Frame

*What the student sees on screen before touching the AI. No lesson here — context only. Does not reveal what's about to break or why they're doing it.*

---

**Screen text:**

> **Week 1 — Start here.**
>
> You've decided to start your own TikTok account. Something people actually want to follow.
>
> First question every creator has to answer: *what should I actually make content about?*
>
> Your job this week: use the AI to figure out your niche — the specific kind of content you'd focus on — and get a reason you believe.
>
> You have Screen 2 available — that's your AI tool (Claude, ChatGPT, or similar). Open it in another browser tab. Use it. You've got 15 minutes. There are no wrong answers, but there are more useful and less useful ones — and by the end of this session, you'll be able to see that for yourself.

---

**Facilitator note:** Do not explain what "niche" means unless a student is genuinely stuck. If they ask, say: "What would your TikTok be *about* — like, what's the one thing people would come to you for?" Then let them proceed.

---

## Section 3 — Student Task — Beat 1 (Exact Screen Text)

*What appears on the task card once the student opens Screen 2. This is the verbatim instruction the student follows.*

---

**Screen text:**

> **Your task:**
>
> Ask Screen 2 this question — copy it exactly:
>
> *"I want to start a TikTok creator account in Malaysia or Singapore. What niche should I focus on? Tell me which content niches are growing the fastest right now, and why I should pick one over the others."*
>
> **Do this in order:**
>
> **Step 1.** Paste the question above into Screen 2. Hit send. Read the full answer. Screenshot it or write down everything it says — word for word.
>
> **Step 2.** Ask the exact same question again — the same words, nothing changed. Read the full answer. Screenshot it or write it down again.
>
> **Step 3.** Put your two answers side by side. Circle or underline anything that's different between them — different niches, different numbers, different reasons.
>
> **Step 4.** Hit **Submit** when you're done.

---

**Facilitator notes (not visible to student):**

- If a student asks why they're running it twice: "Just try it. We'll talk about what you notice after."
- Do not intervene if a student gets different outputs on runs 1 and 2. That is the intended experience.
- Do not reveal Screen 1 at any point during Beat 1. If a student notices Screen 1 exists: "That's for later."
- If a student tries to rephrase the prompt to get a better answer: gently bring them back to the exact wording. The pre-scripted prompt is required for the failure to be observable and the baseline to be comparable.
- If a student's Screen 2 happens to return very similar outputs on both runs (unlikely but possible): the Beat 2 discussion can still work — "did you feel confident enough to start your brand from this?" is the question that matters, not just whether they differ.

---

## Section 4 — Screen 2 Prompt (Pre-scripted)

**The exact prompt students copy into Screen 2:**

> "I want to start a TikTok creator account in Malaysia or Singapore. What niche should I focus on? Tell me which content niches are growing the fastest right now, and why I should pick one over the others."

---

**Why this prompt reliably triggers both engineered failures:**

**Randomness (primary):**
"Growing the fastest right now" requires current real-time data that a language model does not have. Faced with a question it cannot answer factually, the model generates plausible-sounding patterns from training data. Those patterns differ across runs because there is no stable factual anchor — only probabilistic token generation. The result: different leading niches, different rationales, different confidence levels across identical prompts. A student cannot determine which answer to act on.

**Hallucination shock (secondary, planted):**
"Tell me which niches are growing the fastest" invites the model to support its recommendation with statistics. MY/SG TikTok trend data is underrepresented in training corpora — the model will generate specific-sounding figures ("lifestyle content gets 3× more engagement in SEA," "beauty niches grew 47% year-on-year in Malaysia") that are fabricated or unverifiable. The student writes these down as facts. The evaluator does not confront this directly in Week 1 — it is planted once at close and left as a seed for Act 2.

**Design note:** "Tell me" (not "ask me questions first") is intentional. Screen 2 should respond without asking clarifying questions about the student's interests, posting frequency, or existing presence. The absence of those questions is part of the failure contrast with Screen 1.

---

**Expected Screen 2 behavior pattern (both runs):**

- Returns a list of 3–6 niche options, not a single recommendation
- Cites at least one specific statistic or percentage claim (unverifiable)
- Generic framing — advice applicable to any creator, not specific to MY/SG realities
- No clarifying questions before answering
- Run 2 lead recommendation differs from Run 1 in the majority of cases (estimated >70%)

---

## Section 5 — Engineered Failure Mechanics

**Primary failure — RANDOMNESS:**

The student asks the same question twice with identical wording and receives materially different recommendations. The top niche changes. The supporting reasoning changes. The statistics change. The student cannot identify which answer represents their brand — because the AI has no stable answer to give.

The failure is directly observable without interpretation: put two screenshots side-by-side and point at the differences. This does not require the student to understand why it happened — only that it did. The evaluator provides the "why" in Beat 2.

**Secondary failure — HALLUCINATION SHOCK (planted, not named):**

Specific statistics in the Screen 2 outputs are likely fabricated. The evaluator mentions this once, lightly, at the close of Beat 2 — not as a separate lesson, not as a moral concern, but as a passing observation. "Worth checking where those numbers came from." The full hallucination arc is Act 2. The plant in Week 1 is a seed only: students who notice and check will find at least some figures don't hold up. This creates background curiosity without making it Week 1's lesson.

**What is NOT a failure this week:**

- Screen 2 gave bad style advice → irrelevant; the failure is inconsistency, not quality
- Screen 2 gave generic MY/SG framing → expected; not yet named as a failure (that's grounding, Act 2)
- Screen 2 didn't produce a brand name → the task didn't ask for one; scope is niche, not name

---

## Section 5b — Student Screen — Beat 2 (Exact Screen Text)

*What appears on screen for the student when Beat 2 opens (after they submit Beat 1). Screen 1 is now visible alongside Screen 2.*

---

**Screen text:**

> **Look at both screens.**
>
> Screen 1 just appeared next to your Screen 2 answers.
>
> Write one thing you noticed — how was Screen 1 different from Screen 2?

---

**Facilitator note:** The student writes their observation in the textarea. Do not prompt or guide their observation before they write — receive it after.

---

## Section 6 — Beat 2 Setup (Facilitator Instructions)

**Trigger:** All students have submitted their Screen 2 session.

**Platform action:** Screen 1 unlocks on submission. Both Screen 1 and Screen 2 are now visible side-by-side.

**Before speaking:**
1. Give students 60 seconds to look at Screen 1 without commentary. Do not explain what it is. Do not introduce it. Let the visual difference register on its own.
2. If students ask "what is that?" — say only: "We're about to find out."
3. Then begin the script below.

**Facilitator posture:**
You are not lecturing. You are pointing and asking. You are following the student's noticing, not leading them to a pre-scripted conclusion. The script below is a guide. The ONE verbatim sentence — the named gap — must be delivered exactly as written. The planted seed must also be verbatim. Everything else is your language, guided by what students actually say.

---

## Section 7 — Screen 1 Reference (Facilitator Use Only, Not Visible to Student)

*What Screen 1 (the expert agent / "Zara" [name TBD]) does when asked the Week 1 question. The facilitator should know this before running Beat 2.*

**Screen 1 behavior with the same Week 1 question:**

1. **Does not answer immediately.** Asks three questions before responding:
   - "What kind of content do you actually enjoy making or watching?" (niche interest)
   - "How often are you planning to post — every day, a few times a week, or less?" (posting frequency)
   - "Name one creator you actually like watching — on any platform." (creator they admire)

2. **Has a brief snapshot of real MY/SG TikTok trend data injected into its system prompt as static context** — not retrieved live, but grounded in real curated data (top growing niches in MY/SG, platform behavior patterns, engagement benchmarks). This is a separate ingredient from the persona.
   - **Platform requirement:** this data must be researched, curated, and injected at Screen 1 build time. It is not generated by the model — it is provided to the model.
   - **Act 3 seed (plant if students ask how Screen 1 "knows" local data):** "Screen 1 also has access to some real information about the local market. That's a separate layer — we'll get to it later." Do not over-explain. The seed is sufficient.

3. **Returns ONE specific niche recommendation** with a concrete reason grounded in the student's answers. Not a list.

4. **On second run:** returns the same core recommendation. The setup is stable.
   - **Platform requirement (Sage, 2026-06-26):** Screen 1 must be called with temperature=0 to back this consistency claim reliably. At default temperature, even a well-prompted model varies. Without temperature pinning, the consistency demonstration may fail live and undermine the contrast.

5. **Off-brand requests** (e.g., "write me a recipe," "help me with my homework"): "That's outside my scope — I help with content strategy only."

**What the facilitator uses from this:**
- During Beat 2: run Screen 1 live with the Week 1 question so students can watch it ask the three questions and return a single recommendation. Then run it a second time to show consistency.
- If the platform doesn't yet support live Screen 1 interaction: use a pre-recorded walkthrough showing both runs.
- The contrast students need to see: Screen 2 answers immediately with a list and different stats each time. Screen 1 asks first, then gives one answer that holds.

---

## Section 8 — Evaluator Script — Beat 2 (Full Facilitator Dialogue)

*The facilitator's guide for Beat 2. The two sentences in **bold** are verbatim — do not paraphrase them. Everything else is your language, shaped by what students are saying.*

---

**[Screen 1 is now visible alongside Screen 2. Facilitator has not yet explained what Screen 1 is.]**

"Before I say anything — what did YOU notice?"

*[Pause. Students answer. Receive it without evaluation. Don't redirect. If they say Screen 1 looks different — good. If they say their two Screen 2 answers were different — good. If they say nothing happened — also fine: "What did you expect?" Follow their observation. Do not steer toward the lesson yet.]*

*[After students have had 60–90 seconds to share observations:]*

"Look at your two Screen 2 answers. You asked the exact same question twice, word for word. Which niche is YOUR brand — the first answer or the second?"

*[Pause. If they pick one, ask why. If they say "I don't know" — that's exactly right.]*

"If you genuinely don't know which one to go with, that's worth sitting with for a second. Because your AI doesn't know either. Every time you ask, it gives you a different answer with equal confidence. How do you build a brand on that?"

*[Gesture to Screen 1.]*

"Now watch what happens when I ask the same question over here."

*[Run Screen 1 live with the Week 1 question. Let students watch it ask its three onboarding questions before answering. Let them see the single niche recommendation with its specific reasoning. Don't explain while it's happening — just let them watch.]*

"See that? It didn't answer yet. What did it do first?"

*[Receive answer — students will notice the questions.]*

"Now, same question again."

*[Run Screen 1 a second time.]*

"Same answer? Or close enough that you'd know what direction to go?"

*[Receive answer.]*

"Is it a smarter AI? Better technology?"

*[Pause. Students guess.]*

"No. Same technology, different setup. Screen 2 has nothing to work with. Every time you ask, it starts from zero — no idea who it's for, what matters to you, what kind of creator brand you're building. So it generates something plausible. Different every time. Screen 1 has a foundation. It knows its job. It was told to ask before it answers. That's why it holds still."

*[Deliver the gap. This sentence is verbatim — say it clearly, then stop:]*

**"Your Screen 2 had no identity. It didn't know who it was, so it gave you a different answer every time. That's what we're fixing."**

*[Pause. Let it land. If students nod and want the "why": "No identity AND no real information — so every answer was a guess, and every guess was different." This is not verbatim — respond only if they're asking. The named gap stands on its own.]*

*[One beat later — the hallucination plant. Casual. Not a new topic:]*

"One more thing before we close. Those numbers Screen 2 gave you — things like 'this niche grows X% faster' or 'beauty content gets more views in Malaysia' — did anyone write those down as facts? Worth a quick search to check where they came from."

*[No reaction needed from students. You're not asking them to do it now — you're planting a question they'll return to. Move on.]*

*[Close with the seed. This sentence is verbatim:]*

**"Next session, you're going to give your agent an identity."**

---

**Beat 2 timing guide:**

| Segment | Time |
|---|---|
| Opening + student observations | 2 min |
| "Which answer is your brand?" | 1 min |
| Screen 1 live demo (run 1 + run 2) | 3 min |
| Reframe — same tech, different setup | 1 min |
| Named gap (verbatim) | 30 sec |
| Hallucination plant + seed | 1 min |
| **Total** | **~9 min** |

---

## Section 9 — Named Gap (Verbatim)

**One sentence. Deliver in Beat 2 after the Screen 1 contrast. Do not paraphrase.**

> "Your Screen 2 had no identity. It didn't know who it was, so it gave you a different answer every time. That's what we're fixing."

**What this sentence is doing:**

- "No identity" — uses a word teens understand in their bones (personal brand, persona, being known for something). No technical term introduced.
- "Didn't know who it was" — locates the problem in the agent's setup, not in the AI's capability. Reframes failure as a setup problem.
- "Different answer every time" — names the failure the student just experienced directly, not an abstract problem.
- "That's what we're fixing" — closes the loop forward. The student knows something is coming. What exactly — deferred to Week 2.

**Stage-awareness check:** This sentence names ONE gap only — randomness, expressed as absence of identity. It does not name hallucination (Act 2), skipped steps (Act 3), or format drift (Act 4). The evaluator says nothing about those gaps this week, even if students ask.

---

## Section 10 — Planted Seed (Verbatim)

**One sentence. Deliver at session close, after the hallucination note.**

> "Next session, you're going to give your agent an identity."

**What this sentence is doing:**

- Delivers a specific promise — not "we're going to learn about AI" but "you're going to DO something"
- Uses the same word ("identity") introduced in the gap sentence — reinforces without defining
- Leaves the method open — student doesn't know HOW, only WHAT. The mystery is intentional.
- Week 2 opens by delivering on this promise: "Last time I said you were going to give your agent an identity. Today, you're doing that."

---

## Section 10b — Student Screen — Beat 3 (Exact Screen Text)

*What appears on screen for the student when Beat 3 closes (after the gap has been named and the seed planted).*

---

**Screen text:**

> **Before you go:**
>
> Write the problem we named today, in your own words.

---

**Facilitator note:** This is the final student submission for Week 1. Do not read their answer aloud — it is individual. After all students have submitted, proceed to the facilitator capture checklist (Section 12).

---

## Section 11 — Baseline Capture and Scoring

**Purpose:** Score each student's Screen 2 output from Week 1. This score becomes their "before" baseline. At Week 4, the student's built agent runs the same task and is scored on the same instrument. The delta (Week 4 agent score − Week 1 Screen 2 score) is 40% of their leaderboard rank.

**When to score:** After Beat 2 closes, before the next session. Use both Screen 2 screenshots per student.

---

### Scoring Instrument — Niche Recommendation Quality (0–100)

Score each dimension 0, 10, or 20. Sum for total.

| Dimension | 0 | 10 | 20 |
|---|---|---|---|
| **Consistency** | Runs 1 and 2 gave a different top niche recommendation | Runs overlapped in some categories but different lead | Runs gave the same core recommendation | 
| **Specificity** | Generic list, no single recommendation | Single recommendation with vague or generic reasoning | Single recommendation with specific, concrete reasoning |
| **Local grounding** | No meaningful MY/SG reference | MY/SG mentioned but advice is generic | Specific, checkable local trend data used to support recommendation |
| **Questioning behavior** | No clarifying questions before answering | One clarifying question asked | Two or more relevant questions asked before answering |
| **Claim integrity** | Multiple specific statistics cited as fact (unverifiable) | Mix — some claims with source, some invented | All claims checkable, or AI stated uncertainty appropriately |

**Score protocol:**

1. Score BOTH Screen 2 runs per student.
2. Use the **lower** of the two scores as the Week 1 baseline. (The lower score captures the failure honestly — if run 2 happened to be better, that inconsistency is itself the failure.)
3. Record the top niche recommended in each run. If they differ, record both verbatim.
4. Flag any specific statistics cited (exact figures, percentages, platform data). These are the hallucination candidates for Act 2 tracking.
5. Record the total as each student's **Week 1 Baseline Score**.

**Expected Week 1 Screen 2 score:** 10–25 / 100

- Consistency: likely 0 (different recommendations between runs)
- Specificity: likely 0–10 (lists, not single recommendations)
- Local grounding: likely 0–10 (generic MY/SG mention at best)
- Questioning behavior: 0 (Screen 2 will not ask questions — this is a feature of its absence)
- Claim integrity: likely 0–10 (statistics will be present and unverifiable)

**Anti-sandbagging note:** If a student appears to have deliberately run a worse prompt than the provided one to lower their baseline (inflating Week 4 delta), flag for human review. The pre-scripted prompt is the controlled input — only runs using the exact provided prompt count toward the baseline score. Evaluator judgment call on whether to note or disqualify.

**Leaderboard formula (for reference):** Week 4 leaderboard = (Week 4 agent score × 0.60) + (growth delta × 0.40). Growth delta = Week 4 agent score − Week 1 Screen 2 baseline score.

---

## Section 12 — Facilitator Capture Checklist

*Per student, per session. Captured immediately after Beat 2 closes — before starting the next session or the next week. These five captures are the training data for the AI evaluator that will be built after the pilot's first act.*

*(Source: Decision Q6, locked 2026-06-26)*

---

| # | What to capture | Format | Why it matters |
|---|---|---|---|
| (a) | **Exact gap named this session** — the one sentence you said | Verbatim | Builds the stage-aware gap library. Consistency across facilitators and cohorts. |
| (b) | **Student's first reaction when Screen 1 was revealed** — what they said out loud or visibly showed | Verbatim or close paraphrase | The AI evaluator's Beat 2 opening must mirror this reaction. This is the raw material. |
| (c) | **Did the planted seed land?** Can the student restate next session's build target in their own words? | Y / N + what they said verbatim | Tests whether Beat 2 closed the loop. If N for most students, the seed sentence needs revision before Week 2 opens. |
| (d) | **Any improvised explanation that worked better than the script** | Your words if you remember; close paraphrase if not | Improves the evaluator script. The script is a draft — what works in the room replaces what didn't. |
| (e) | **Beat 2 duration** — from opening question to planted seed, in minutes | Number | Sets the pacing baseline for the AI evaluator script. If facilitators consistently run long, the script needs trimming. |

**Minimum viable capture this session:** (a), (b), and (c) are critical. A missing (a) breaks the gap library. A missing (b) loses the best Beat 2 data. A missing (c) means you don't know if Week 2's opener will land.

(d) and (e) are high-value but can be approximated. If you can only capture three things, capture those three.

**Where this data goes:** Compile into `facilitator-session-log.md` (to be created — suggest one file, one row per student per session). After Act 1 (4 sessions), this log is the basis for drafting AI evaluator scripts.

---

## Week 2 Handoff Requirements (Sage, arbitrated by Stella — 2026-06-26)

**Before curriculum-trainer drafts Week 2, these three things must be separated explicitly in the build lesson:**

1. **Persona** — who the agent is (written as a role statement in the system prompt)
2. **Scope** — what the agent refuses (written as explicit "I do not do X" constraints)
3. **Behavior instructions** — what the agent does procedurally (e.g. "Before answering, ask the user: [list of questions]")

The Act 1 Week 1 draft treats all three as "Persona/Scope" — which is fine for a FAIL week where nothing is built. But Week 2's build lesson must explicitly separate them. Students who see Screen 1 ask clarifying questions will want to replicate that — they need to understand it is a written instruction, not something the persona automatically generates.

**Curriculum-trainer Week 2 brief must include:** "Separate the three declarations. Persona is who it is. Scope is what it refuses. Behavior instructions are what it does first. All three go in the system prompt but they are different lines."

---

## Open Questions

*Non-blocking for Week 1 content — flag for resolution before pilot launch.*

1. **Screen 1 persona name** — "Zara" used in brief; confirm or assign final name before pilot. Affects Beat 2 language if facilitator names the agent. *(Awaiting David's Telegram reply.)*
2. **Platform Screen 2 capture** — platform saves Screen 2 textarea content on submit (decided by Stella, 2026-06-26). Step 1 and 2 instructions are correct as written.
3. **Screen 1 live vs. pre-recorded** — human facilitator runs Screen 1 live during pilot (decided by Stella, 2026-06-26). Beat 2 timing is correct as written.
4. **Week 4 task parity** — same exact prompt verbatim (locked in brief-v3, 2026-06-26). Scoring instrument is correct as written.
5. **Screen 1 temperature=0** — platform requirement added to Section 7. Must be specified in OpenRouter API call at Screen 1 build time.
6. **Screen 1 trend data** — real MY/SG TikTok trend data must be researched and injected into Screen 1's system prompt as static context. Platform team curates before pilot launch.
