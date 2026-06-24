import json
from typing import Any, List, Optional

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    payload: Any
    artifact_refs: Optional[List[Any]] = None


class SubmissionOut(BaseModel):
    id: str
    exercise_id: str
    attempt_number: int
    status: str
    submitted_at: str


class ScenarioResultOut(BaseModel):
    scenario_id: str
    passed: bool
    detail: Optional[str] = None


class RubricScoreOut(BaseModel):
    criterion_id: str
    met: bool
    score: float
    confidence: Optional[float] = None
    severity: Optional[str] = None
    evidence: Optional[str] = None


class EvaluationResultOut(BaseModel):
    submission_id: str
    schema_version: str
    ran: bool
    scenario_results: Optional[List[ScenarioResultOut]] = None
    rubric_scores: Optional[List[RubricScoreOut]] = None
    overall_score: float
    productive_failure_signal: str
    detected_approach: Optional[str] = None
    confidence: Optional[float] = None
    passed: bool
    feedback_markdown: Optional[str] = None
    judge_model: str
    judge_escalated: bool
    usage: Optional[Any] = None
    cost_micro_usd: Optional[int] = None
    evaluated_at: str


class SubmissionDetailOut(SubmissionOut):
    result: Optional[EvaluationResultOut] = None
