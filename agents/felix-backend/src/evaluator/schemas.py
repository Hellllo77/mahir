"""Pydantic models for structured LLM-judge output (ADR-003).

These are used with client.messages.parse() / structured outputs so the judge
result is valid-by-construction — no fragile parsing.
"""
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ScenarioResult(BaseModel):
    scenario_id: str
    passed: bool
    detail: str


class RubricScore(BaseModel):
    criterion_id: str
    met: bool
    score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    severity: Literal["minor", "major", "critical"]
    evidence: str = Field(description="Must cite a Stage-1 transcript/output; no ungrounded claims.")


class JudgeOutput(BaseModel):
    """Structured output the LLM judge produces — valid-by-construction via structured outputs."""

    schema_version: str = "1.0"
    ran: bool
    scenario_results: List[ScenarioResult] = []
    rubric_scores: List[RubricScore] = []
    overall_score: float = Field(ge=0.0, le=1.0)
    productive_failure_signal: Literal["productive", "low_effort", "off_task"]
    detected_approach: Optional[str] = Field(
        default=None,
        description="ApproachTaxonomy.code — the solution approach detected in this submission.",
    )
    confidence: float = Field(ge=0.0, le=1.0)
    passed: bool
    feedback_markdown: str = Field(
        description="Learner-facing, PF-aware feedback. Failure is expected and fine; focus on what was explored."
    )
