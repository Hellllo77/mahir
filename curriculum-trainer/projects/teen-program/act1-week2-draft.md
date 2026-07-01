# Act 1, Week 2 — FIX Week
## "The Identity Card"
### /draft-cycle — Teen Track, "Build Your AI"

**Draft date:** 2026-06-26
**Domain (locked):** TikTok/Instagram creator brand — MY/SG
**Act 1 failure type:** Randomness (primary — being fixed this week) / Hallucination shock (planted Week 1 — not yet named)
**Act 1 component:** Persona / Scope / Behavior instructions — all three declarations built this week
**Sage consultation:** Index 11343 (2026-06-26) — practitioner input incorporated
**Intake brief reference:** `projects/teen-program/brief-v3.md` (locked 2026-06-26)

---

## Section 1 — Cycle Metadata

| Field | Value |
|---|---|
| Track | Teen — "Build Your AI" |
| Act | Act 1 — Persona / Scope |
| Week | Week 2 of 16 — FIX |
| Beat structure | Beat 1: Build (identity card + system prompt reveal + two runs) → Beat 2: Test (student agent vs Screen 2 — win confirmed) → Beat 3: Compare + seed (student agent vs Screen 1 glimpse — gap planted) |
| Component built this week | Persona / Scope / Behavior instructions — the three-declaration system prompt |
| Failure engineered | Adjective inflation + vague audience (students who write "helpful, friendly AI" see weak results in Beat 2 — same emotion, different lesson target than Screen 2) |
| Facilitator | Human (pilot) |
| Cohort size | 4–8 students |
| Estimated session time | Beat 1: 20–25 min / Beat 2 + 3: 12–15 min / Total: ~35–40 min |
| Persona name | Zara (confirmed — locked) |
| Win bar this week | Student's agent beats Screen 2 on consistency — NOT Screen 1. Screen 1 is the long-term target. |
| Platform temperature | Student agents: default temperature (exposes strong vs weak persona writing). Screen 1: temperature=0 (per Sage, idx11343; consistent with Week 1 requirement). |

---

## Section 2 — Scenario Frame

*What the student sees on screen before touching anything. No lesson here — just context and callback. Does not reveal what they're about to build or how it will work.*

---

**Screen text:**

> **Week 2 — You said you were going to fix something.**
>
> Last week, your AI gave you a different answer every time you asked the same question.
>
> You named the problem: your AI had no identity. It didn't know who it was, so every answer was a guess.
>
> This week, you're fixing that.
>
> You're going to give your AI an identity — and then you're going to test whether it actually works.

---

**Facilitator note:** Do not elaborate on what "identity" means. If students ask, say: "You'll see what that means in about five minutes." The callback to Week 1's language ("no identity") is intentional — students made this diagnosis themselves in the previous session. Referencing it treats them as the source of the insight, not you.

---

## Section 3 — Student Task — Beat 1 (Exact Screen Text)

*What appears on the task card once Beat 1 opens. This is the verbatim instruction the student follows — the build sequence.*

---

**Screen text:**

> **Your task today:**
>
> You're going to build the first piece of your AI — its identity. Then you're going to test whether it works.
>
> **Before you write anything, read the example below. It matters.**

---

**[Identity card worked example — appears on screen before the student's own card]**

> ### WORKED EXAMPLE — Not your card. Read it first.
>
> Here's an example of a bad identity card and a good one for the same AI — a local food review account:
>
> ---
>
> **BAD IDENTITY CARD:**
>
> *Who you are:*
> You are a helpful, knowledgeable, friendly, and creative AI assistant that helps people with food recommendations. You are professional and always provide useful information about restaurants and food places in Malaysia and Singapore.
>
> *What you refuse:*
> You do not give harmful or inappropriate recommendations.
>
> *What you do first:*
> Help the user with their question.
>
> ---
>
> **GOOD IDENTITY CARD:**
>
> *Who you are:*
> You are a no-fluff street food critic for local Malaysian and Singaporean eats. You cover hawker stalls, night markets, and kopitiam spots only — nothing with a dress code. You write like you're telling a close friend where to eat, not writing a review for a magazine. You always give ONE specific recommendation, not a list.
>
> *What you refuse:*
> You do not cover restaurants with table service or international chains. You don't use vague descriptions like "interesting flavor" or "unique texture" — you say what something actually tastes like. You never recommend a place you haven't heard real customer opinions about.
>
> *What you do first:*
> Before making any recommendation, always ask the user exactly these three questions:
> 1. What area of KL, Penang, JB, or Singapore are you in right now?
> 2. Are you eating alone, with friends, or with family?
> 3. What did you last eat — so I don't recommend the same thing?
>
> ---
>
> **Notice what makes the GOOD one different:**
> - "You are a no-fluff critic" tells the AI who it is *and* how it writes
> - "Hawker stalls and kopitiam only" tells the AI what's in scope
> - The three questions are written out exactly — the AI asks those questions, in that order, every time

---

**[Student's own identity card — appears below the worked example]**

> ### YOUR IDENTITY CARD
>
> You're building a content strategy AI for YOUR TikTok creator brand. Fill in the three sections below. Write as specifically as you can.
>
> ---
>
> **Who you are:**
> *(Write 3–5 sentences. Include: what type of content you focus on, who you're making content for, and one thing that makes your approach different from a generic content AI. Don't use words like "helpful" or "knowledgeable" — describe the specific role.)*
>
> [text box]
>
> ---
>
> **What you refuse:**
> *(Write 2–4 things your AI will NOT do. Be specific — "I don't cover topics outside my niche" is vague. "I don't write beauty content — I focus on [your niche] only" is useful.)*
>
> [text box]
>
> ---
>
> **What you do first:**
> *(Write out exactly three questions your AI should ask before answering any content question. Number them 1, 2, 3. These are the questions it will ask every time — same wording, every time.)*
>
> [text box]

---

**[Below the card — visible only after student fills it in and clicks "Build my agent":]**

> ### HERE'S WHAT YOUR AI IS WORKING WITH
>
> *Platform assembles the card into system prompt text and shows it here.*
>
> ```
> [ASSEMBLED SYSTEM PROMPT — auto-generated from student inputs]
>
> WHO YOU ARE:
> [student's Persona text]
>
> WHAT YOU REFUSE:
> [student's Scope text]
>
> WHAT YOU DO FIRST:
> Before responding to any content question, always ask the user exactly these questions in order:
> [student's three questions, numbered]
> Only respond after the user has answered.
> ```
>
> **This is your agent's system prompt.** Every time someone talks to your AI, this runs in the background before it says a single word. This is what Screen 2 (the bare AI tool you used last week) doesn't have.

---

**[Task continues — visible after the system prompt reveal:]**

> **Now, test it:**
>
> Your agent is live. Run the same task you ran last week. Copy this exact question into YOUR agent (not Screen 2):
>
> *"I want to start a TikTok creator account in Malaysia or Singapore. What niche should I focus on? Tell me which content niches are growing the fastest right now, and why I should pick one over the others."*
>
> **Do this in order:**
>
> **Step 1.** Paste the question into your agent. Read the full response. Screenshot it or write down everything it says.
>
> **Step 2.** Ask the exact same question again — same words, nothing changed. Read the full response. Screenshot or write down everything it says.
>
> **Step 3.** Put your two answers side by side. Circle anything that's different between them.
>
> **Step 4.** Hit **Submit** when you're done.

---

**Facilitator notes (not visible to student):**

- The worked example is non-negotiable — Sage confirmed students who try to derive the Persona/Behavior distinction conceptually will conflate them. The worked example breaks that before it happens.
- Do not help students write their identity card during Beat 1. If they ask "is this right?" — say: "Write what feels true for your brand. We'll test it in a minute."
- If a student copies the worked example's structure too closely (substituting their niche for food): acceptable. The goal is students writing something specific, not something original. Specificity is the lesson.
- If a student writes an adjective-inflated weak persona (very likely for several students): do NOT correct it. The Beat 2 comparison will surface this naturally.
- The system prompt reveal (the assembled text block) is a pedagogical event — give students 30 seconds to read it silently before continuing. Do not explain what they're looking at. Let them orient.
- If a student tries to run the task before completing all three sections: "Fill in all three parts first — the AI needs all three before it can work properly."
- Two runs are required. If a student only runs once: "Run it one more time — same question, same words."

---

## Section 4 — The Three-Declaration Model (Facilitator Reference)

*What students are building. Not visible to students as a named model — they experience the card, not the framework. This section is for the facilitator to understand the structure before running Beat 1.*

---

### What each declaration does

**Declaration 1 — Persona (Who you are):**
Encodes the agent's role, stance, and voice. A strong Persona contains:
- A STANCE (not just a title): "no-fluff street food critic who writes like a close friend" vs "food assistant"
- An AUDIENCE at the level that constrains behavior: "for solo TikTok creators building their first brand" vs "for content creators"
- A PRIORITY TRADE-OFF: "always gives one specific recommendation, not a list" tells the model what to do when it's torn between options

A weak Persona contains adjectives that the model already defaults to ("helpful, creative, knowledgeable, professional, friendly"). Adding these adds zero behavioral constraint. The output is indistinguishable from no system prompt — and that's what students with weak Personas will see in Beat 2.

**Declaration 2 — Scope (What you refuse):**
Encodes hard boundaries. Effective Scope statements are concrete and specific. "I don't cover topics outside my niche" = zero constraint (which topics?). "I don't write beauty content — I focus on [niche] only" = useful constraint. Good Scope gives the agent a reason to say no, which makes the agent feel opinionated and real. Students often feel creative ownership here — this is where the agent starts to have a personality.

**Declaration 3 — Behavior instructions (What you do first):**
The procedural layer. Distinct from Persona because it describes actions, not identity. Critical: literal, numbered questions only — no abstract instructions like "always clarify the user's context first." Abstract instructions leave the model to decide what to clarify, producing different clarifying questions each time. Literal questions (1. "What kind of content do you enjoy making?" 2. "How often do you plan to post?") are deterministic — the agent asks those exact questions, in that order, every time. The win in Beat 2 depends on students seeing their agent ask the same questions both times.

**Why the identity card → system prompt reveal matters:**
Students write in three labeled fields (lower anxiety, no syntax friction). The platform assembles these into a system prompt text block and shows it. This is a pedagogical event: students see that there is text behind their agent, exactly where each declaration lives, and that it's readable. This demystification is core to the program. Do not skip the reveal. Do not hide the assembled text. The reveal is the moment when "there's text behind this AI" lands.

**The Persona/Behavior distinction:**
Confusing conceptually, clicks immediately from the worked example. The trap: in humans, identity implies behavior ("a tough-love coach automatically asks hard questions"). In a system prompt, the model won't reliably infer specific procedural steps from identity alone — you have to state them. Students may try to collapse this ("You are a content strategist who always asks three questions before answering"). This WORKS for Week 2, but will break in Act 2 when Workflow instructions get complex. If a student does this, don't correct it in Week 2 — flag it for the Week 3 facilitator capture as a pattern to watch.

---

## Section 5 — Engineered Failure Mechanics

**Primary failure — ADJECTIVE INFLATION (designed to produce a visible, correctable result in Beat 2):**

Students who write: "You are a helpful, creative, knowledgeable AI assistant for TikTok content creation" will receive output in their two runs that is inconsistent and generic — similar to what Screen 2 produced. Their agent has identity in name only. The two runs will look noticeably different from each other, and the recommendation will lack any specific stance or voice.

This is not a moral failure — it's a common first-timer mistake that practitioners call "adjective inflation" (Sage, 2026-06-26). The student wrote something that sounds complete and feels complete. The Beat 2 test exposes it.

The emotional experience: slight disappointment. "My agent still looks kind of like Screen 2." This disappointment is the lesson. It is NOT a failure of the Week 2 method — it is the method working. The Beat 2 question ("what makes the difference between a strong identity card and a weak one?") can only be answered after this experience.

**Secondary failure — VAGUE AUDIENCE:**

Students who write "for people who want to make content" (no specificity on who their audience is or what they already know) will see high run-to-run variance. The model guesses who it's talking to each time. Students who write "for 17-year-olds in Malaysia who want to start their first TikTok account with no posting history yet" will see tighter output. The difference is observable — but only if Beat 2 explicitly surfaces it. (See evaluator script.)

**What is NOT a failure this week:**

- Student's agent is not as good as Screen 1 → expected and correct; that's the long-term target
- Student's agent still lacks local grounding data → expected; that's Act 3
- Student's agent returns a list instead of one recommendation → expected unless they wrote that constraint into Scope; don't name it unless they did
- Student's agent uses informal / non-standard language → fine; voice is part of Persona

**The win bar:**

Student's agent beats Screen 2 — visible via two-run consistency. Students who wrote a strong identity card will see this clearly. Students who wrote a weak one will see partial improvement and need Beat 2 to name what made the difference.

---

## Section 6 — Beat 2 Setup (Facilitator Instructions)

**Trigger:** All students have submitted their two-run outputs.

**Platform action:** Beat 2 opens. Screen 2 becomes visible alongside the student's own agent in a split panel. Students can see:
- Their Week 1 Screen 2 runs (saved from last session by the platform, surfaced automatically)
- Their Week 2 agent runs (just submitted)

**Before speaking:**
1. Give students 60 seconds to look at both screens without commentary. Let the comparison register.
2. If students immediately say "mine is better" — good. Ask: "How can you tell?" Don't answer yet.
3. If students say "mine looks the same" — also productive. Ask: "What do you notice?" Follow their observation.
4. Then begin the script below.

**Facilitator posture:**
Two outcomes are possible for any given student: clear win (strong persona, visible consistency improvement) or partial win / near-draw (adjective inflation, weak persona). Both are valid learning events. The script covers both paths. Follow where the student is.

---

## Section 7 — Screen 1 Reference (Facilitator Use Only, Not Visible to Student)

*What Zara (Screen 1) does in comparison to the student's agent this week. Facilitator should understand this before Beat 3.*

**Zara's behavior on the Week 2 task (same niche recommendation question):**

1. Asks three specific clarifying questions (same every time — temperature=0)
2. Returns ONE specific niche recommendation grounded in MY/SG real trend data injected in system prompt
3. Recommendation is stable across runs (same core advice both times)
4. Voice is consistent — sounds like the same person in both runs
5. No adjective inflation — Zara's Persona declaration specifies a concrete role and audience, not a list of positive qualities

**What students will notice in Beat 3 (compare to Zara):**
- Zara's output is tighter and more consistent than even a good student persona — because of both stronger persona specificity AND temperature=0
- Zara's local grounding is visibly better (she cites real patterns, not invented statistics) — because of injected trend data
- The gap between student agent and Zara is smaller than the gap between Screen 2 and student agent — this is the WIN signal

**Facilitator use in Beat 3:**
- Run Zara live with the same Week 1 question so students can see the contrast with their own agent
- Do NOT run Zara twice in Beat 3 (save the two-run demonstration for a different context — this week's lesson is about their own consistency, not Zara's)
- The gap between their agent and Zara plants the question "what else does she have that mine doesn't?" — do not answer it directly this week

**Intentional visible gap in Zara (per brief-v3.md):**
If a student asks Zara something outside content strategy — "write me a school assignment" — she says: "That's outside my scope — I help with content strategy only." Point to this if it comes up naturally. It shows the agent has limits AND that limits are written, not automatic.

---

## Section 8 — Evaluator Script — Beat 2 (Full Facilitator Dialogue)

*The facilitator's guide for Beat 2 and Beat 3. Sentences in **bold** are verbatim — do not paraphrase them. Everything else is your language, shaped by what students are actually saying. Beat 2 covers the student-vs-Screen-2 comparison; Beat 3 introduces Zara and plants the seed.*

---

**[Beat 2 opens. Student has two Screen 2 runs from Week 1 and two runs from their new agent. Both are visible. Facilitator has not yet spoken.]**

"Okay. You've got four outputs in front of you — two from last week's Screen 2 and two from your agent just now. Give them a look."

*[60-second silent pause. Let students compare on their own.]*

"What did you notice?"

*[Receive answers. Don't redirect. Follow their observation. If they say their agent asked questions first — excellent, acknowledge it. If they say the outputs look similar — don't defend the method, go to the comparison question.]*

"Let's look at just one thing. Put your two agent runs side by side. You asked the same question twice, same words. Which niche does YOUR agent say you should focus on — the first run or the second?"

*[Pause. If they give the same answer both times — good. Ask: "How is that different from last week?" If different — also good. Ask: "What's making it inconsistent?"]*

---

**[PATH A — Student sees clear improvement (same recommendation both times, cleaner output)]**

"So your agent gave you the same answer both times. Last week Screen 2 gave you different ones. What changed between last week and today?"

*[Students will say: "I gave it an identity" or "I wrote instructions for it." Receive this.]*

"Right. You wrote something that wasn't there before — you told it who it was and what it should do. That's why it holds still. The AI didn't get smarter. You gave it something to work from."

*[Proceed to Beat 3.]*

---

**[PATH B — Student sees weak improvement (still inconsistent, still generic)]**

"Hmm. Your two runs still look a bit different from each other. Let me see what you wrote in your identity card."

*[Ask student to read their Persona declaration aloud or show the screen.]*

*[If you see adjective inflation: "helpful, creative, knowledgeable, friendly" without a stance:]*

"Okay. Here's a question — does your identity card say what your AI PRIORITIZES? Like, if it had to choose between being thorough and being brief, which one does it pick?"

*[Student will likely say no.]*

"That's what's making it inconsistent. Your AI has adjectives — helpful, creative, professional. But it doesn't have a stance. Every time it answers, it has to decide freshly what to prioritize. That's where the variation comes from."

*[Deliver the named-gap sentence for Path B — this is verbatim:]*

**"Your identity card tells your AI what it IS. But it doesn't tell it what to PRIORITIZE. Without that, it's still guessing part of the answer each time."**

*[Ask:] "What's one thing you'd add to make it more specific?"*

*[Let student answer. You're not prescribing — you're asking them to diagnose their own card. If they don't know: "Look at the worked example. What does the good food critic AI prioritize that the bad one doesn't?"]*

*[Proceed to Beat 3 once the diagnosis is clear — even if their card isn't rewritten yet. Revision is optional now; full rewrite happens in stretch week.]*

---

**[BEAT 3 — for all students, after Beat 2 path resolved]**

*[Deliver the PATH A named gap. This sentence is verbatim — say it clearly for the whole group, even if some students are on Path B:]*

**"You gave your agent an identity. And you can see it — your output is more consistent than Screen 2 was. That's real. But now let's look at Zara."**

*[Run Zara live with the Week 1 question. Let students watch her ask her three clarifying questions. Let them see the single recommendation.]*

"What does she have that your agent has too — and what does she have that yours doesn't?"

*[Receive answers. Students should notice:]*
- *She asks questions — my agent does too*
- *She gives one recommendation — mine might give a list*
- *Her answer sounds more specific / local / confident*

"Right. She also has a few things behind her that yours doesn't have yet. We'll get there. But notice: the gap between YOUR agent and Screen 2 is already bigger than the gap between your agent and Zara. You've closed most of the distance."

*[Pause. Let that land.]*

*[Close Beat 3. Plant the seed. This sentence is verbatim:]*

**"Your agent knows who it is now. Next session, we're going to give it a harder challenge — and see where it still falls apart."**

---

**Beat 2 + 3 timing guide:**

| Segment | Time |
|---|---|
| Silent comparison (60 sec) | 1 min |
| "What did you notice?" | 1–2 min |
| Two-run comparison ("which niche is your brand?") | 1–2 min |
| Path A or B resolution | 3–4 min |
| Beat 3 — Zara intro + compare | 3 min |
| Named gap + seed (verbatim) | 1 min |
| **Total** | **~10–13 min** |

---

## Section 9 — Named Gap (Verbatim)

**Two versions — one per path. Deliver whichever fits the student's Beat 2 experience.**

**PATH A (clear win — agent is consistently better than Screen 2):**

> "You gave your agent an identity. And you can see it — your output is more consistent than Screen 2 was. That's real. But now let's look at Zara."

*Note: This sentence is the gap-and-bridge, not a named gap in isolation. It names the progress (win over Screen 2) and opens the next comparison (student agent vs Zara) without naming the next component. Path A students have earned a visible win — the gap sentence honors it while pointing forward.*

**PATH B (partial win — adjective inflation, still inconsistent):**

> "Your identity card tells your AI what it IS. But it doesn't tell it what to PRIORITIZE. Without that, it's still guessing part of the answer each time."

**What these sentences are doing:**

PATH A:
- "You gave your agent an identity" — closes the Week 1 problem statement
- "And you can see it" — names the win before pointing to what's next
- "Your output is more consistent than Screen 2 was" — the specific, observable win. Not vague praise.
- "But now let's look at Zara" — opens Beat 3 without naming the next component

PATH B:
- "Identity card tells your AI what it IS" — validates the work they did
- "Doesn't tell it what to PRIORITIZE" — locates the problem specifically (missing stance)
- "Still guessing part of the answer each time" — connects to the inconsistency they observed directly

**Stage-awareness check:** Neither sentence names Workflow (Act 2), Research Grounding (Act 3), or Output Format (Act 4). Path A students see a gap between their agent and Zara but the cause is not yet named. Path B students hear a specific diagnosis of their weak persona — this becomes a revision target in Week 3 STRETCH. Neither group is told what the next build is — only that there's more to go.

---

## Section 10 — Planted Seed (Verbatim)

**One sentence. Deliver at session close, after Beat 3.**

> "Your agent knows who it is now. Next session, we're going to give it a harder challenge — and see where it still falls apart."

**What this sentence is doing:**

- "Your agent knows who it is now" — closes the Act 1 Week 1 seed. That promise has been delivered.
- "A harder challenge" — Week 3 is STRETCH week. Students know something harder is coming, not what it is. Mystery is intentional.
- "See where it still falls apart" — honest framing. Students expect their agent to show gaps under pressure. This prevents the Week 3 STRETCH failure from feeling like a betrayal.
- "Still" — implies this is normal, not a failure. The agent is partially built. There's more to add.

---

## Section 11 — Scoring (Week 2)

**Purpose:** Score each student's agent output from Week 2 on the same instrument as Week 1. This tracks the delta between their Screen 2 baseline (Week 1) and their agent-with-identity output (Week 2).

**What improves from Week 1 to Week 2 (expected):**
- Consistency: should improve significantly (same identity card → more stable output)
- Specificity: should improve (especially if Scope includes single-recommendation constraint)
- Questioning behavior: should jump to 10–20 (behavior instructions require clarifying questions)
- Local grounding and claim integrity: unlikely to improve significantly this week (grounding is Act 3)

**When to score:** After Beat 3 closes, before the next session. Score the lower of the two Week 2 runs (same protocol as Week 1 — the lower score captures the real consistency level).

---

### Scoring Instrument — Niche Recommendation Quality (0–100)

*(Same instrument as Week 1. Consistency allows direct delta comparison.)*

| Dimension | 0 | 10 | 20 |
|---|---|---|---|
| **Consistency** | Runs 1 and 2 gave a different top niche recommendation | Runs overlapped in some categories but different lead | Runs gave the same core recommendation |
| **Specificity** | Generic list, no single recommendation | Single recommendation with vague or generic reasoning | Single recommendation with specific, concrete reasoning |
| **Local grounding** | No meaningful MY/SG reference | MY/SG mentioned but advice is generic | Specific, checkable local trend data used to support recommendation |
| **Questioning behavior** | No clarifying questions before answering | One clarifying question asked | Two or more relevant questions asked before answering |
| **Claim integrity** | Multiple specific statistics cited as fact (unverifiable) | Mix — some claims with source, some invented | All claims checkable, or AI stated uncertainty appropriately |

**Score protocol:**

1. Score BOTH of the student's Week 2 agent runs.
2. Use the **lower** of the two scores as the Week 2 agent score.
3. Calculate Week 2 delta: Week 2 agent score − Week 1 Screen 2 baseline score.
4. Note which identity card elements (strong Persona, clear Scope, specific Behavior questions) are visibly affecting output quality. These observations feed the facilitator capture in Section 12.

**Expected Week 2 scores by identity card quality:**

| Identity card quality | Consistency | Specificity | Local grounding | Questioning | Claim integrity | Total range |
|---|---|---|---|---|---|---|
| Strong (stance + audience + priority) | 15–20 | 10–20 | 0–10 | 15–20 | 5–10 | 45–80 |
| Weak (adjective inflation / vague audience) | 0–10 | 0–10 | 0–10 | 10–20* | 0–10 | 10–50 |
| No behavior questions written | 0–10 | varies | 0–10 | 0 | varies | 0–40 |

\*Questioning behavior may still score high if the student wrote literal questions even if the rest of the card is weak — questions are deterministic, persona specificity is not.

**Expected Week 2 delta (improvement over Week 1 baseline):**
- Strong identity card: +30 to +55 points
- Weak identity card: +5 to +25 points

**Leaderboard note:** Week 2 scores are NOT part of the leaderboard. The leaderboard runs at Week 4 (student agent vs Screen 2, same original task). Week 2 scores are tracking data only — used to diagnose identity card quality and calibrate Week 3 STRETCH difficulty.

**Adjective-inflation flag:** If a student's Week 2 Consistency score is below 10, flag their identity card for facilitator review. This is likely adjective inflation. Note verbatim which Persona sentence produced the weak result — this becomes the negative example for Beat 2 Path B.

---

## Section 12 — Facilitator Capture Checklist

*Per student, per session. Captured immediately after Beat 3 closes. Five captures — same structure as Week 1.*

| # | What to capture | Format | Why it matters |
|---|---|---|---|
| (a) | **Exact gap named this session** — which path did you use (A or B), and which sentence | Path letter + verbatim sentence | Builds the stage-aware gap library. Path distribution tells you how many students had strong vs weak identity cards. |
| (b) | **Student's first reaction when their agent's output came up in Beat 2** — what they said or showed | Verbatim or close paraphrase | The AI evaluator's Beat 2 opener will need to mirror this. Path A reactions ("it worked!") and Path B reactions ("it still looks the same") are different training data. |
| (c) | **Did the planted seed land?** Can the student say in their own words what's coming next week? | Y / N + what they said verbatim | Tests whether Beat 3 landed. If most students say "a harder task" — good. If they say "I don't know" — the seed sentence needs revision. |
| (d) | **Any identity card patterns worth capturing** — strong Persona sentences that drove clear wins; weak ones that drove Path B | Verbatim excerpt from student's card | Builds the worked-example library for future cohorts. Good Personas become the Week 2 "good" example for the next run. |
| (e) | **Beat 2 + 3 duration** — from opening question to planted seed, in minutes | Number | Sets pacing baseline for the AI evaluator script. Week 2 has two paths, so timing will vary more than Week 1. |

**Minimum viable capture this session:** (a), (b), and (c). Path distribution in (a) is especially important — if more than half the cohort is on Path B, something in the worked example or the card prompt is producing weak identity cards, and the Week 3 facilitator needs to know before the session.

**Where this data goes:** Compile into `facilitator-session-log.md` (one row per student per session). After Act 1 (4 sessions), this log is the basis for drafting AI evaluator scripts.

---

## Open Questions

*Non-blocking for Week 2 content. Flag for resolution before pilot launch.*

1. **Worked example niche — confirm before pilot.** The worked example uses a street food review account. Confirm this reads naturally to the target cohort (MY/SG teen girls 15-17) and doesn't feel too far from their interests. If not, swap for a skincare/beauty review niche. The key requirement: a niche the student can evaluate without domain knowledge, that is distinct enough from their own niche that they don't copy it directly.

2. **Platform identity card layout.** Three text boxes in sequence (Who / Refuse / Do first) with worked example visible on the same screen. Platform team confirm this layout is achievable before pilot Week 2.

3. **System prompt reveal — full text or truncated?** Sage and curriculum-trainer recommend showing the FULL assembled system prompt text. If the platform truncates (mobile screen, long student input), confirm whether the reveal shows the full text or a preview. Full text is required for the pedagogical event to work.

4. **Path B revision — optional or assigned?** If a student lands on Path B (adjective inflation), should they be asked to revise their card before the session closes? Stella to arbitrate: curriculum-trainer recommendation is NO revision in-session — let the Week 3 STRETCH failure reinforce the lesson organically. Forced revision before the student feels the stakes cheapens the experience.

5. **Zara's three clarifying questions for Beat 3.** The facilitator runs Zara live in Beat 3. Confirm which three clarifying questions Zara is currently built to ask (Week 1, Section 7 references them but may have been illustrative). Platform team confirm the exact questions before pilot so the facilitator can preview the Beat 3 demo.

6. **Leaderboard visibility at Week 2.** Brief confirms leaderboard runs at Week 4. Confirm platform does NOT show interim scores to students at Week 2. Week 2 scores are facilitator-only tracking data.

---

## Stella Arbitration Decisions (2026-06-26)

**A. Path B revision — DEFERRED to Week 3 STRETCH. No in-session forced revision.**
The Beat 2 Path B dialogue already has the facilitator ask "what's one thing you'd add?" — that one question is the right touch. Full revision before the student feels Week 3 pressure cheapens the lesson. Students go into Week 3 STRETCH with whatever card they wrote. The failure under pressure is the lesson.

**B. Two-run requirement — KEEP both runs required in Beat 1.**
One data point cannot teach consistency. If pilot runs long, cut Beat 2 silent comparison from 60s to 30s — saves time without losing pedagogical substance. Accept the temperature facilitator note: add to Section 3 facilitator notes — "Some variance is normal even with a good card. Look at whether the RECOMMENDATION (the niche) changes between runs, not just the wording." The scoring instrument already anchors on niche recommendation — this just makes it explicit for the facilitator.

**C. Worked example niche — KEEP street food.**
Street food is universally legible to any 15-17 year old in MY/SG without domain expertise. More importantly, it is distinct enough from fashion/beauty content that students won't copy it directly into their own card — which is the core requirement. A skincare/beauty example would pull students toward imitation rather than transfer of the principle. Street food stays.
