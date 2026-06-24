---
name: research
description: Use to search for current, industry-specific evidence before
  drafting curriculum content. Triggered automatically as part of /intake for
  any corporate session, and for any teen session requiring current venture-context
  evidence. Also triggered manually when the user asks to "research [topic],"
  "find examples of [process]," "check whether [claim] is accurate," or "look up
  current [industry] practices." Do not fabricate industry examples, process
  descriptions, or factual claims — research them. Update lessons-learned.md
  after every session.
allowed-tools: Read, Write, WebSearch, WebFetch
---

# Research Skill

Searches for current, credible, industry-specific evidence to ground curriculum
content in reality. Prevents drafts from being built on priors or invented
examples.

## When to Use

As part of `/intake` for every corporate session. Manually via `/research
$ARGUMENTS` where `$ARGUMENTS` names the topic, industry, or process type.

## Process

### Step 1: Load prior research
Read `references/lessons-learned.md` — prior sessions may have already
researched this industry or process type. Use what's there; do not rediscover.

### Step 2: Define the research targets
Before searching, name what you are looking for:

- What does this process actually look like in this industry, in practice?
- What are the realistic AI failure modes in this specific context?
- What vocabulary does this audience use for this work?
- What would "real business standards" mean for an evaluator judging this work?
- Are there recent examples of companies using (or misusing) AI for this process?

### Step 3: Search
Run searches scoped to the last 12–18 months. Prefer:
- Industry association publications and reports
- Practitioner write-ups from credible publications
- Official documentation (tool vendors, regulatory bodies where relevant)

Avoid: SEO-bait listicles, undated content, vendor marketing, AI-generated
summaries, content that cites no primary source.

Run at minimum 3 searches per research target. If first results are thin,
broaden the query — try the job function rather than the industry.

### Step 4: Compile findings
Summarise findings per research target. For each finding:
- State the finding in plain language
- Name the source (publication, author, date)
- Note its relevance to the failure mechanic being designed

Verify: each research target has at least one finding with a named, datable
source. No finding is presented without a source. Where sources conflict, name
the conflict — do not silently pick one.

### Step 5: Flag evidence gaps
If a research target returns insufficient credible results, mark it explicitly:
"Insufficient evidence for [target] — proceed with caution." Do not fill the
gap by inventing an example.

### Step 6: Save to lessons-learned
Append a lesson entry to `references/lessons-learned.md` covering: what was
researched, what was found (top 2–3 findings with sources), and any gaps.

Verify: entry is appended, not overwriting existing content.

## If This Fails

- **No fresh results for the industry:** Try the job function instead of the
  industry label (e.g. "accounts payable clerk recurring tasks" instead of
  "manufacturing back-office"). Try adjacent industries with similar processes.
- **All results are vendor marketing:** Add a publication filter — search
  specifically within LinkedIn articles, Harvard Business Review, McKinsey,
  industry-specific trade publications. Append `-site:vendor.com` to exclude
  known SEO domains if needed.
- **WebFetch returns a paywall:** Try the publisher's summary page, or search
  for a secondary citation of the same finding from a different source. Do not
  fabricate from the title alone.
- **Process type is so niche that no published material exists:** Flag this to
  the owner. A process with no published failure-mode evidence is harder to
  engineer a reliable failure for — the owner may need to supply a subject-matter
  expert.
- If none of the above work, search online for:
  "[industry] [job function] AI automation failure examples 2025 2026"

After resolving, update `references/lessons-learned.md` with what worked.
