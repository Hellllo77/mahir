"""Stage 2 — LLM judge pipeline (ADR-003).

Pre-filter (Haiku) → main judge (Sonnet) → optional escalation (Opus)
when confidence < threshold. Runs via OpenRouter (openai-compatible API).
API keys never enter the sandbox — all model calls are host-side.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

import openai

from src.config import settings as _settings
from src.evaluator.schemas import JudgeOutput

_JUDGE_SYSTEM = """\
You are an expert evaluator for an agent-building learning platform that uses Productive Failure (PF) pedagogy.

Evaluate the learner's submitted agent build against the rubric and Stage-1 sandbox transcript.

Rules:
- Ground every rubric score in evidence you can cite from the Stage-1 transcript. No ungrounded claims.
- PF signal meanings:
  - 'productive': learner made real attempts with at least one identifiable approach
  - 'low_effort': empty, trivial, or random submission with no genuine engagement
  - 'off_task': completely unrelated to the exercise prompt
- detected_approach must be a code from the provided ApproachTaxonomy list, or null if none applies.
- feedback_markdown is shown to the learner: keep it encouraging and focus on what was explored.
"""

_JUDGE_JSON_INSTRUCTION = """\
Output ONLY valid JSON with this exact structure (no markdown fences):
{
  "schema_version": "1.0",
  "ran": <bool>,
  "scenario_results": [{"scenario_id": <str>, "passed": <bool>, "detail": <str>}, ...],
  "rubric_scores": [{"criterion_id": <str>, "met": <bool>, "score": <0.0-1.0>, "confidence": <0.0-1.0>, "severity": <"minor"|"major"|"critical">, "evidence": <str>}, ...],
  "overall_score": <0.0-1.0>,
  "productive_failure_signal": <"productive"|"low_effort"|"off_task">,
  "detected_approach": <str or null>,
  "confidence": <0.0-1.0>,
  "passed": <bool>,
  "feedback_markdown": <str>
}
"""

# Micro-USD per token (1 USD = 1,000,000 micro-USD; prices are per million tokens)
_PRICING: dict[str, tuple[float, float, float, float]] = {
    # tier: (input, output, cache_write, cache_read)
    "haiku":  (1.0,  5.0,  1.25, 0.10),
    "sonnet": (3.0, 15.0,  3.75, 0.30),
    "opus":   (5.0, 25.0,  6.25, 0.50),
}


@dataclass
class _Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

    def absorb(self, usage) -> None:
        self.input_tokens += getattr(usage, "prompt_tokens", 0) or 0
        self.output_tokens += getattr(usage, "completion_tokens", 0) or 0
        # Cache token fields not exposed via OpenRouter/OpenAI SDK
        self.cache_creation_input_tokens += 0
        self.cache_read_input_tokens += 0

    def cost_micro_usd(self, tier: str) -> int:
        inp, out, cw, cr = _PRICING[tier]
        return int(
            self.input_tokens * inp
            + self.output_tokens * out
            + self.cache_creation_input_tokens * cw
            + self.cache_read_input_tokens * cr
        )


def _tier(model_id: str) -> str:
    if "haiku" in model_id:
        return "haiku"
    if "sonnet" in model_id:
        return "sonnet"
    return "opus"


def _build_exercise_context(
    exercise_prompt: str,
    scenarios: list[dict],
    rubric_criteria: list[dict],
    approach_codes: list[str] | None,
) -> str:
    lines = ["## Exercise Prompt", exercise_prompt.strip(), ""]
    lines += ["## Rubric Criteria"]
    for c in rubric_criteria:
        lines.append(f"- [{c['code']}] {c['description']} (weight={c.get('weight', 1.0):.2f})")
        if c.get("guidance_markdown"):
            lines.append(f"  Guidance: {c['guidance_markdown']}")
    lines += ["", "## Test Scenarios (Stage-1 ran these)"]
    for s in scenarios:
        lines.append(
            f"- {s['id']}: input={json.dumps(s.get('input_payload', {}), separators=(',', ':'))}"
        )
    if approach_codes:
        lines += ["", f"## Valid ApproachTaxonomy codes: {', '.join(approach_codes)}"]
    return "\n".join(lines)


def _get_client(api_key: str | None = None) -> openai.AsyncOpenAI:
    return openai.AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
    )


async def _prefilter(client: openai.AsyncOpenAI, transcript_bundle: str, submission_payload: dict) -> tuple[bool, _Usage]:
    """Fast Haiku classification — genuine attempt or junk?"""
    usage = _Usage()

    payload_preview = json.dumps(submission_payload, separators=(",", ":"))[:2000]
    transcript_preview = transcript_bundle[:3000]

    resp = await client.chat.completions.create(
        model=_settings.judge_model_prefilter,
        max_tokens=128,
        timeout=30.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a classifier. Respond ONLY with 'GENUINE' or 'NOT_GENUINE', "
                    "followed by a colon and one short reason (≤15 words)."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Submission payload:\n{payload_preview}\n\n"
                    f"Stage-1 transcript:\n{transcript_preview}\n\n"
                    "Is this a genuine attempt at building an agent for the exercise? "
                    "GENUINE = contains real code/logic/structure. "
                    "NOT_GENUINE = empty, random text, or completely off-task."
                ),
            },
        ],
    )
    usage.absorb(resp.usage)

    text = resp.choices[0].message.content or ""
    return text.strip().upper().startswith("GENUINE"), usage


async def _run_judge(
    client: openai.AsyncOpenAI,
    exercise_context: str,
    transcript_bundle: str,
    submission_payload: dict,
    model: str,
) -> tuple[JudgeOutput, _Usage]:
    """Structured LLM judge via OpenRouter — returns parsed JudgeOutput."""
    usage = _Usage()

    payload_str = json.dumps(submission_payload, indent=2)[:4000]

    resp = await client.chat.completions.create(
        model=model,
        max_tokens=8192,
        timeout=30.0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": _JUDGE_SYSTEM + "\n" + _JUDGE_JSON_INSTRUCTION,
            },
            {
                "role": "user",
                "content": (
                    f"{exercise_context}\n\n"
                    f"## Submission Payload\n```json\n{payload_str}\n```\n\n"
                    f"## Stage-1 Transcript\n{transcript_bundle}"
                ),
            },
        ],
    )
    usage.absorb(resp.usage)

    content = resp.choices[0].message.content or "{}"
    result = JudgeOutput.model_validate_json(content)
    return result, usage


async def judge_submission(
    submission_payload: dict,
    transcript_bundle: str,
    scenarios: list[dict],
    rubric_criteria: list[dict],
    exercise_prompt: str,
    approach_codes: list[str] | None = None,
    api_key: str | None = None,
    preferred_model: str | None = None,
) -> tuple[JudgeOutput, dict]:
    """Pre-filter → main judge → optional Opus escalation.

    api_key: org-scoped OpenRouter key; falls back to OPENROUTER_API_KEY env var.
    preferred_model: org-scoped default model; falls back to settings.judge_model_default.
    Returns (JudgeOutput, metadata) where metadata has usage + cost fields
    matching EvaluationResult columns.
    """
    client = _get_client(api_key)
    default_model = preferred_model or _settings.judge_model_default
    escalated = False

    # Pre-filter
    is_genuine, pf_usage = await _prefilter(client, transcript_bundle, submission_payload)

    if not is_genuine:
        result = JudgeOutput(
            schema_version="1.0",
            ran=True,
            scenario_results=[],
            rubric_scores=[],
            overall_score=0.0,
            productive_failure_signal="low_effort",
            detected_approach=None,
            confidence=0.95,
            passed=False,
            feedback_markdown=(
                "Your submission doesn't appear to contain a genuine agent build. "
                "Please submit code or configuration that addresses the exercise prompt."
            ),
        )
        return result, {
            "judge_model": _settings.judge_model_prefilter,
            "escalated": False,
            "usage_input_tokens": pf_usage.input_tokens,
            "usage_output_tokens": pf_usage.output_tokens,
            "usage_cache_read_tokens": pf_usage.cache_read_input_tokens,
            "cost_micro_usd": pf_usage.cost_micro_usd("haiku"),
        }

    # Main judge (Sonnet / org preferred model)
    exercise_context = _build_exercise_context(
        exercise_prompt, scenarios, rubric_criteria, approach_codes
    )
    judge_result, judge_usage = await _run_judge(
        client, exercise_context, transcript_bundle, submission_payload,
        model=default_model,
    )

    # Escalate to Opus when confidence is below threshold
    esc_usage = _Usage()
    if judge_result.confidence < _settings.judge_escalation_threshold:
        escalated = True
        esc_result, esc_usage = await _run_judge(
            client, exercise_context, transcript_bundle, submission_payload,
            model=_settings.judge_model_escalation,
        )
        if esc_result.confidence >= judge_result.confidence:
            judge_result = esc_result

    used_model = _settings.judge_model_escalation if escalated else default_model
    cost = (
        pf_usage.cost_micro_usd("haiku")
        + judge_usage.cost_micro_usd("sonnet")
        + (esc_usage.cost_micro_usd("opus") if escalated else 0)
    )
    total_input = pf_usage.input_tokens + judge_usage.input_tokens + esc_usage.input_tokens
    total_output = pf_usage.output_tokens + judge_usage.output_tokens + esc_usage.output_tokens
    total_cache_read = (
        pf_usage.cache_read_input_tokens
        + judge_usage.cache_read_input_tokens
        + esc_usage.cache_read_input_tokens
    )

    return judge_result, {
        "judge_model": used_model,
        "escalated": escalated,
        "usage_input_tokens": total_input,
        "usage_output_tokens": total_output,
        "usage_cache_read_tokens": total_cache_read,
        "cost_micro_usd": cost,
    }
