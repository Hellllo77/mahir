import json
from typing import Any, List, Optional

from pydantic import BaseModel


class PfGateConfig(BaseModel):
    min_attempts: int = 2
    min_distinct_approaches: int = 2
    min_exploration_seconds: int = 300
    allow_fast_unlock: bool = True


class ExerciseSummary(BaseModel):
    id: str
    title: str
    sequence_index: int
    phase: Optional[str] = None


class ModuleOut(BaseModel):
    id: str
    title: str
    sequence_index: int
    summary_markdown: Optional[str] = None
    exercises: List[ExerciseSummary] = []


class ExerciseOut(BaseModel):
    id: str
    module_id: str
    title: str
    sequence_index: int
    prompt_markdown: str
    facilitator_notes_markdown: Optional[str] = None
    build_spec: Any
    prerequisite_exercise_ids: List[str] = []
    gate: PfGateConfig


class ConsolidationContentOut(BaseModel):
    exercise_id: str
    body_markdown: str
    reference_build: Optional[Any] = None
    check_questions: Optional[List[Any]] = None
