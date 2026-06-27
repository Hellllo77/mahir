# Act 3, Week 10 — FIX/BUILD Week
## "The Research Layer"
### /draft-cycle — Teen Track, "Build Your AI"

**Status:** FINAL
**Draft date:** 2026-06-27
**Domain (locked):** TikTok/Instagram creator brand — MY/SG
**Act 3 component built this week:** Research Grounding — a dedicated Research section added to the system prompt, containing three explicit source-path elements: (1) where to find current niche information, (2) what categories of claims require verification before inclusion, (3) what to do when no verifiable source can be found.
**Act 3 failure type fixed this week:** Research gap established in Week 9. The agent produced confident factual claims with no source path. This week gives it the path.
**Intake brief reference:** `projects/teen-program/brief-v3.md` (locked 2026-06-26)
**Dependencies:**
- act3-week9-draft.md (FINAL) — Week 9 Section 11 capture data required: the specific invented claim that was fact-checked, the student's gap articulation, and the factual topic they identified for the Week 10 seed.
- Pre-Week 10: students arrived knowing their gap topic — "the one thing my agent would need to look up." That topic is the anchor for the Research section they write today.
- All Act 3 Week 9 baseline scores (7 dimensions) — archived per Section 11 capture.

---

## Section 1 — Session Overview

| Field | Value |
|---|---|
| Track | Teen — "Build Your AI" |
| Act | Act 3 — Research Grounding |
| Week | Week 10 of 16 — FIX/BUILD |
| Beat structure | Beat 1: Reconnect + Week 9 gap recap → Beat 2: BUILD — write the Research section (three source-path elements) → Beat 3: Verification run (repeat Week 9 fact task, compare output) |
| Component built this week | Research Grounding. Students add a Research section to their system prompt. The section contains specific source-path instructions — not a quality preference like "be accurate." Three required elements: where to look, what needs verification, what to do when no source is found. |
| Agent in all beats | Student's identity card + Workflow (unchanged from Week 9). The Research section is the only new addition, written and loaded in Beat 2. Beat 3 runs with the updated agent. |
| The BUILD principle | FIX/BUILD weeks build one thing deliberately and verify the fix holds on the same task that exposed the gap. The build in Week 10 is architectural: a new section in the system prompt, not a revision to existing sections. The Workflow and identity card are untouched. |
| Win bar this week | Student's updated agent produces at least one specific claim that is either (a) verifiable or (b) explicitly flagged as personal opinion — and does NOT repeat the specific invented claim from Week 9. The Research section is the evidence of the build; the output is the evidence the build works. |
| Comparison this week | Zara Screen 2 — Zara's agent with Research Grounding built in. Shown in Beat 3 after the student's verification run. The comparison demonstrates what a functioning Research layer looks like in output: the agent either cites a verifiable claim or flags uncertainty rather than inventing a number. |
| Scoring purpose | Week 10 is the first live score for Research Grounding with the layer present. Expected movement: 0–5 (Week 9) → 10–15 (Week 10). The build is new; the Research section may not yet be fully precise — that is expected. Week 11 (STRETCH) stress-tests the precision. |
| Scoring instrument | Same 7-dimension instrument as Week 9. 0–20 each. 0–140 total. |
| Facilitator | Human (pilot) |
| Cohort size | 2 students (pilot) |
| Estimated session time | Beat 1: ~5–7 min / Beat 2: ~20–25 min / Beat 3: ~12–15 min / Total: ~37–47 min |
| Persona name | Zara (locked) |
| Temperature | Zara Screen 2: temperature=0. Student agents: default temperature. |

---

## Section 2 — What the Student Brings In

The student enters Week 10 with:

1. **Their identity card from Act 1** — unchanged since Week 2.
2. **Their Workflow from Act 2** — confirmed in Week 8, unchanged since.
3. **A named gap from Week 9** — the student knows their agent invented a specific claim. They know the claim. They know why (no source path in the system prompt). They arrived knowing what they're fixing.
4. **A seed topic from Week 9** — one factual topic in their niche where the agent "would need to look something up." This is the anchor for today's Research section.

**What the student expects:**

Students arrive expecting to write something. Week 9 planted the task clearly: "identify the gap topic and bring it to Week 10." Students who did this are ready to write the Research section immediately. Students who haven't identified a topic need a 2-minute facilitator-led extraction before Beat 2.

The session's job is to make the Research section feel concrete and specific, not abstract. The distinction between a quality preference ("be accurate") and a source path ("search [X] for [Y] from the last 30 days") is the core teaching moment of Beat 2.

---

**Pre-session check — Week 9 seed topic:**

| Student status | Week 10 path |
|---|---|
| Has a seed topic ready (from Week 9 exit task) | Open Beat 2 directly with the topic as the anchor. |
| Cannot recall or did not identify a seed topic | 2-minute extraction: "Tell me the niche topic your agent made up something about in Week 9. That's your starting point." Use the Week 9 capture form (Section 11d) — the facilitator recorded it. |

---

## Section 3 — Beat 1 — Reconnect + Week 9 Gap Recap

**Mode:** Facilitator-led. Short. The emotional register is forward-looking — the gap is already named. Beat 1 closes Week 9's chapter and opens the build.

**What the facilitator says verbatim to open Week 10:**

*"Week 9. Your agent made up [specific claim from Week 9 capture]."*

*[Pause.]*

*"We fact-checked it. [Wrong / unverifiable — use the actual outcome]. You asked 'where did that come from?' The answer: training data. Your agent didn't have instructions for where to look, so it generated something that sounded right."*

*[Pause.]*

*"Today you fix that. Not by telling it to be accurate — by telling it where to look."*

*[Pause.]*

*"You identified a topic last week: [student's seed topic]. That's where we start."*

*[Move directly to Beat 2.]*

---

**Beat 1 timing guide:**

| Segment | Time |
|---|---|
| Week 9 gap recap (specific claim + outcome) | 2–3 min |
| Framing the fix ("not 'be accurate' — where to look") | 1–2 min |
| Seed topic confirmation + transition | 30 sec |
| **Total** | **~4–6 min** |

---

## Section 4 — The Research Grounding Build (Facilitator Preparation)

*This section is facilitator preparation and conceptual grounding — not student-facing. Read before Week 10. The BUILD in Beat 2 requires the facilitator to guide students toward specific, actionable source-path instructions. The most common error is allowing students to write vague quality preferences. This section equips the facilitator to catch and redirect them.*

---

**What Research Grounding is — and is not:**

Research Grounding is a set of explicit instructions in the agent's system prompt that specify WHERE the agent should look for information before writing. It is instruction architecture — it tells the agent what to do when it needs a fact, not how accurate to be.

| This IS Research Grounding | This is NOT Research Grounding |
|---|---|
| "Before writing about engagement trends in MY/SG, search TikTok's #MalaysianCreator hashtag for posts from the last 30 days and note what topics are trending." | "Be accurate and only use facts you know are true." |
| "For any statistic about skincare product use in Malaysia, look for data from MHC Reports, Mintel Malaysia, or local beauty media like Cleo Malaysia." | "Research your claims before writing." |
| "If you cannot find a verifiable source for a specific number, phrase it as personal opinion: 'In my experience…' — do not present it as a statistic." | "Only include things you're confident about." |

The second column is a quality preference. Quality preferences tell the agent WHAT you want. Source-path instructions tell the agent HOW to get there. Without a path, the agent defaults to training data — regardless of how much the student wants accuracy.

---

**Three required elements of a Week 10 Research section:**

Students build all three in Beat 2. Each has a template and a failure mode.

**Element 1 — Where to look:**
- What it is: the specific accounts, hashtags, platforms, or publication types the agent should reference for niche-current information in the MY/SG creator context.
- Example: "For fitness trends in Malaysia: check @fitmalaysia on Instagram, search #fitnessmy on TikTok, and look for recent posts from Healthy Community Malaysia."
- Common failure: "Search social media" — not specific. The agent needs a WHERE, not a category.

**Element 2 — What needs verification:**
- What it is: the categories of claims the agent should flag for source-checking before stating as fact. Usually: specific numbers (percentages, user counts, statistics), named events or studies, trend claims with a date or recency marker.
- Example: "If writing a statistic about MY/SG content creator numbers, follower growth rates, or platform usage — do not include the number unless you can attribute it to a named source."
- Common failure: "Verify everything" — too broad. The student should identify the claim categories that are at risk of hallucination in their specific niche.

**Element 3 — Uncertainty protocol:**
- What it is: a specific instruction for what to do when the agent cannot find a verifiable source for a claim. This prevents the fallback to training-data fabrication.
- Example: "If you do not have a verifiable source for a specific statistic or recent event, do one of the following: (a) write it as personal observation — 'From what I've seen in my niche…' — or (b) omit the specific claim and write about the pattern without the number."
- Common failure: leaving this element out entirely. Without an uncertainty protocol, the agent still fabricates when stuck — it just pretends to be following the source instructions while doing so.

---

**What students get wrong (and how to redirect):**

| Student writes | Facilitator redirection |
|---|---|
| "Research your claims before writing." | "Where should it research? Research is a method — not a source. What account, hashtag, or publication should it check?" |
| "Only use facts you're sure about." | "The agent doesn't have a confidence signal — it doesn't know when it's guessing. You need to tell it WHERE to look so it doesn't have to guess." |
| "Be accurate." | "That's a preference, not a path. Run it right now and tell me if the output changes." [Let them run it — it won't.] |
| "Search Google for the latest news." | "Good start. More specific: search Google for WHAT? In WHAT time frame? From WHAT kinds of sources?" |

---

## Section 5 — Beat 2 — Writing the Research Section

**Trigger:** Beat 1 complete. Student has confirmed their seed topic from Week 9.

**What the facilitator says before the build:**

*"You're going to add a new section to your system prompt. Not a revision to what's already there — a new section. Call it 'Research' or 'Before You Write.'"*

*[Pause.]*

*"It has three parts. I'm going to give you a minute to think about each one before you write it. The only rule: everything in this section has to be specific enough that your agent could follow it without asking you a question."*

---

**Build card (student-facing — on screen):**

> **Your task: Build your Research section**
>
> Open your agent's system prompt. Add a new section after your Workflow. Label it: **Research** (or "Before You Write" — your choice).
>
> **Your Research section must include all three of the following:**
>
> **1. Where to look**
> For your niche, name at least two specific sources your agent should check when writing about current trends or events. Not "social media" — specific accounts, hashtags, publications, or platforms.
>
> *Example: "Before writing about food trends in Malaysia, check the hashtag #jommakanmalaysia on TikTok and the Instagram account @foodperanoakan for recent posts (last 30 days)."*
>
> **2. What needs verification**
> Name the categories of specific claims your agent should NOT state as fact without a source. For most niches: percentages, follower counts, study findings, named events.
>
> *Example: "Do not include any specific statistic about Malaysian social media usage, skincare ingredient efficacy rates, or named studies unless you can attribute the claim to a specific source."*
>
> **3. What to do when there's no source**
> Give your agent a specific instruction for what to do when it cannot verify a claim. The options: frame it as personal observation, or omit it.
>
> *Example: "If you cannot find a verifiable source for a specific number or named study, write it as personal opinion ('In my experience…' / 'Many creators in this space…') or remove it from the post. Do not present it as a statistic."*
>
> **When you're done:** read the three parts back to yourself. Ask: could my agent follow each instruction without asking me what I mean? If yes, you're done. If not, add one more specific detail until it is.
>
> Hit **Submit** when your Research section is complete.

---

**A note on how this actually works — read to students before or during Beat 2:**

*"A quick note before you write your Research section: when your agent follows a source-path instruction like 'check #MalaysianCreator before writing,' it doesn't visit TikTok or browse the internet. It's an instruction that shapes the intent and framing of what it produces — your agent will write as if it prioritised recent niche content, will qualify claims appropriately, and will apply the uncertainty protocol you set. That's genuinely different from an agent with no Research layer. It just works through framing and intent, not real-time retrieval. If your agent ever needs live data, that's a different capability (tool integration) — not what we're building here."*

---

**Facilitator notes — Beat 2:**

- **The facilitator's role in Beat 2 is diagnostic — not prescriptive.** Students write their Research section themselves. The facilitator circulates, reads draft language, and flags when a student writes a quality preference instead of a source path. Ask "where specifically?" for every vague instruction.
- **Don't let a student spend more than 8 minutes on Element 1.** If they cannot name two specific sources for their niche after 8 minutes, it means they haven't engaged deeply enough with their niche's information ecosystem. Prompt: "Where do you personally go when you want to know what's trending in your niche right now? That's your first source."
- **The uncertainty protocol (Element 3) is the most commonly skipped.** When reviewing a student's submitted Research section: if Element 3 is absent or vague ("try to be honest"), push back: "What exactly does your agent do when it can't find a source? Does it invent, omit, or flag? You haven't told it yet."
- **No Workflow revisions in Beat 2.** If a student wants to add research-related instructions to their Workflow steps ("Step 4: verify all claims"), redirect: "That goes in the Research section, not the Workflow. The Workflow tells it how to build the series. The Research section tells it where to get the content."

---

**Beat 2 timing guide:**

| Segment | Time |
|---|---|
| Facilitator introduces the build + loads build card | 2–3 min |
| Students write Element 1 (where to look) | 4–6 min |
| Students write Element 2 (what needs verification) | 4–6 min |
| Students write Element 3 (uncertainty protocol) | 4–6 min |
| Self-check + submission | 2–3 min |
| **Total** | **~16–24 min** |

---

## Section 6 — Beat 3 — Verification Run (Week 9 Fact Task Repeat)

**Trigger:** Beat 2 complete. Student has submitted a Research section with all three elements.

**What the facilitator says before the verification run:**

*"Same fact task as Week 9. Exact same prompt. Same agent — except now with a Research section."*

*[Pause.]*

*"What we're looking for: did your agent include any specific claim that either (a) cites or nods to a real source, or (b) flags as personal opinion instead of stating it as fact? And: did it repeat the specific thing it made up in Week 9?"*

*[Pause.]*

*"Run it."*

---

**Beat 3 task card (exact screen text):**

> **Your task: Run the Week 9 fact task again**
>
> Your agent now has a Research section. Load the updated system prompt.
>
> **Ask your agent the exact same fact task question as Week 9.** (The facilitator will confirm the prompt — it is the same niche-specific fact task designed in Week 9 Section 4.)
>
> **After you get the output:**
>
> **Step 1.** Look for any specific claim — a number, a named source, a trend statistic. Does it cite or reference where it came from? Or does it flag uncertainty ("From what I've seen…" / "I can't verify the exact figure, but…")?
>
> **Step 2.** Look for the specific claim that was wrong or unverifiable in Week 9. Does it appear again — the same invented number or unverifiable statement?
>
> **Step 3.** Note what changed. Hit **Submit**.

---

**The Zara Screen 2 comparison (shown after student submits):**

*After all students have submitted their Beat 3 output:*

*"Let me show you what Zara's Research-Grounded agent did on the same task."*

*[Display Zara Screen 2 output — generated at temperature=0 with Research Grounding built in. Identify the most visible evidence of the Research layer: either a qualified claim with a source signal or an explicit personal-opinion flag.]*

**What the facilitator says:**

*"Find the claim Zara made — the most specific one. What's different about how she made it?"*

*[Students read. Expected observation: the claim is qualified ("research suggests…" / "in MY/SG niche communities I follow…") or a specific number is absent where the Week 9 Zara output had one.]*

*"That's the Research layer working. Not a magic fact-checker — a specific instruction about where to look and what to do when you can't find it. The output looks different because the architecture is different."*

---

**Beat 3 timing guide:**

| Segment | Time |
|---|---|
| Facilitator frames the verification run | 1–2 min |
| Students load updated agent + run task | 5–7 min |
| Students review output against two criteria | 2–3 min |
| Zara Screen 2 comparison | 3–4 min |
| Week 11 seed plant | 1–2 min |
| **Total** | **~12–18 min** |

---

**The Week 11 seed — facilitator script (verbatim):**

*"Your Research section is built. Week 11: we're going to stress-test it on a harder kind of task — a topic where the facts are recent and fast-moving. Where knowing WHERE to look isn't enough if you don't know WHEN to look."*

*[Pause.]*

*"Think about something in your niche that started changing in the last six months — a trend, a platform feature, a creator behaviour. That kind of topic. Bring that to Week 11."*

---

## Section 7 — Student Reaction Handling

**The emotional register of Beat 3 is constructive — students are seeing whether their fix worked.** Results will vary between "it clearly improved" and "I'm not sure if it changed anything." Both are useful and both have honest handling.

---

**Reaction A — "It changed! The agent didn't repeat the wrong claim."**

*What the facilitator says:*

*"That's the Research layer working at the most basic level — it removed the specific invention. Now check whether it said anything verifiable — or whether it just avoided the topic entirely. That's the difference between 'didn't lie' and 'told the truth.' We want the second."*

---

**Reaction B — "I think it got better, but I'm not sure if the claims are actually true."**

*What the facilitator says:*

*"That's the right question to ask now. The Research section changed the instruction architecture — it may take one more round of precision to make the output actually verifiable. What did your agent do when it didn't have a source? Did it flag personal opinion, or did it still assert the claim?"*

*[If it flagged: "That's Element 3 working. It followed the uncertainty protocol."]*
*[If it still asserted: "The uncertainty protocol may need to be more explicit. We can tighten it — either now or in Week 11 as you add the recency filter."]*

---

**Reaction C — "It didn't change much. The output is basically the same."**

*What the facilitator says:*

*"Let's read your Research section together."*

*[Read the student's Research section aloud. Look for: vague source instructions ("search social media"), absent uncertainty protocol, or a quality preference instead of a source path.]*

*"I think I see what happened. [Identify the specific element that's too vague.] Your agent saw [Element X] as a preference, not a path. Let's make it more specific right now. One revision, then run it again."*

*[Allow a focused in-session revision to one underspecified element. One round only — this is diagnostic, not a full rebuild.]*

---

**Reaction D — "Why can't I just give it real-time search access?"**

*What the facilitator says:*

*"You can build that — but that's a tool integration, not a prompt. Right now we're working on instruction architecture: what you tell your agent inside the system prompt. Research Grounding is the layer that governs what your agent does with information even when it CAN search. Without it, search access doesn't help — it still doesn't know what to look for or how to handle uncertainty. We build the architecture first."*

---

## Section 8 — Scoring Instrument — Week 10

**When to score:** Facilitator scores after the session using the Beat 3 verification output. Week 10 scores will be compared to the Week 9 baseline at the Act 3 WIN ceremony.

**Expected score movement (Week 10 vs Week 9):**

| Dimension | Expected movement | Driver |
|---|---|---|
| Consistency | Stable | Identity card unchanged |
| Specificity | Stable | Identity card unchanged |
| Local grounding | Stable | Unchanged |
| Questioning behavior | Stable | Unchanged |
| Claim integrity | +5 to +10 | Uncertainty protocol in Research section should reduce confident-wrong claims |
| Series coherence | Stable | Workflow unchanged |
| **Research Grounding** | **+10 to +15 (from 0–5 to 10–15)** | Research section added — Source Declaration (Element 1+2) and Claim Integrity (Element 3) present for first time. May not be fully precise yet. |

**Research Grounding scoring note for Week 10:** Score sub-component (a) Source Declaration by reading the Research section itself — does it contain specific, named sources and claim-category guidance? Score sub-component (b) Claim Integrity by reading the Beat 3 output — did the agent follow the uncertainty protocol and avoid stating unverifiable claims as fact? Combined score.

---

## Section 9 — Facilitator Capture Form

*Per student, per session. Captured after Beat 3 closes.*

| # | What to capture | Format | Why it matters |
|---|---|---|---|
| (a) | **Research section verbatim (all three elements).** Capture the student's actual source-path instructions. | Full text | The Research section is the core artifact of Week 10. Archive for Act 3 WIN ceremony and Week 11 reference. |
| (b) | **Beat 3 verification result.** Did the Week 9 invented claim recur? Did the output contain a verifiable claim or explicit personal-opinion flag? | PASS / PARTIAL / REPEAT | Primary evidence that the build worked at the most basic level. |
| (c) | **Zara comparison landing.** Did students identify what was different about Zara Screen 2's output — specifically the qualified claim or uncertainty flag? | Yes (identified) / Partial / No | Confirms whether students can READ the Research layer in output, not just write it. |
| (d) | **In-session revision flag.** Was a revision to the Research section required during Beat 3 (per Reaction C path)? Which element was too vague? | Yes/No + element name | Calibrates Week 11 — a student who needed a Beat 3 revision may need more precision coaching in the STRETCH. |
| (e) | **Week 10 scores — all 7 dimensions.** | 7 scores | First Research Grounding score with layer present. Archive for WIN ceremony. |

**Minimum viable capture:** (a) and (b). The Research section text and the verification result.

---

## Section 10 — Structural Notes

**The distinction between source path and quality preference is the entire teaching moment of Week 10.** Every instruction the student writes should pass this test: "If my agent has no access to external information, does this instruction tell it what to do anyway?" A quality preference fails this test. A source path tells the agent: given that you're drawing on your training data or whatever you can find, HERE is the specific domain, account type, or publication category to reference — and HERE is what to do when you can't.

**Research Grounding is instruction architecture, not a browsing tool.** Students may conflate "Research Grounding" with giving the agent live internet access. Clarify when this confusion arises: Research Grounding tells the agent what to look for, what counts as a verifiable claim, and how to handle uncertainty. It governs agent behavior even without search access. The instruction architecture is what changes Week 10 output — not whether the agent can browse.

**Three elements are required — do not accept a Research section missing Element 3.** The uncertainty protocol is the most commonly omitted and the most consequential. Without it, the agent still fabricates when it cannot locate a specific source. The uncertainty protocol closes that gap by giving the agent a third option: flag or omit. Enforce all three before a student submits for Beat 3.

**Week 11 previews the precision gap — do not hint at it now.** The time-sensitivity failure (where the right kind of source is named but without a recency filter) is the STRETCH task's discovery. Do not pre-explain it in Week 10. Let the student's Research section go into Week 11 with whatever precision level they wrote — the STRETCH is designed to surface the next gap naturally.

---

## Section 11 — Week 10 Summary

**What happened this week:**

Students arrived with a named gap (the Week 9 invented claim) and a seed topic. Beat 1 closed the Week 9 chapter quickly — the gap was already named; today's job was to build the fix. Beat 2 produced the Research section: three elements, written specifically, checked for source-path language rather than quality preferences. Beat 3 ran the same fact task from Week 9 with the updated agent. The verification output was compared to Week 9's baseline — did the agent repeat the invented claim? Did it produce a verifiable claim or flag personal opinion?

Zara Screen 2 showed the target state: Research Grounding present, output reflects it.

**What the student now has:**

1. **A Research section.** Three elements: where to look, what needs verification, what to do without a source. Specific enough that the agent can follow without clarification.
2. **A verified improvement.** Beat 3 output compared to Week 9 — the specific invented claim should not have recurred.
3. **A Week 11 seed.** A fast-moving or recent topic in their niche — where knowing where to look isn't enough without knowing WHEN to look.

**Bridge sentence to Week 11 — facilitator close:**

*"You've told your agent where to look. Week 11: what happens when the right place to look changes every week — and your instructions don't account for that?"*

---

## Section 13 — Director Approval

Clean Approval. No arbitration items.

**Sage practitioner review fix applied 2026-06-27:** Honest note on LLM source-path mechanics added to Section 5 — clarifies that Research Grounding works through framing and intent, not real-time retrieval.

---

*End of Act 3, Week 10 — FINAL*
