from typing import List, Optional

from pydantic import BaseModel


class PfGateConfig(BaseModel):
    min_attempts: int = 2
    min_distinct_approaches: int = 2
    min_exploration_seconds: int = 300
    allow_fast_unlock: bool = True


class ExerciseProgressOut(BaseModel):
    id: Optional[str] = None
    exercise_id: Optional[str] = None
    phase: str
    attempts_total: int = 0
    attempts_genuine: int = 0
    distinct_approaches: int = 0
    exploration_seconds: int = 0
    explored: bool = False
    unlocked_at: Optional[str] = None
    completed_at: Optional[str] = None
    mastery_score: Optional[float] = None
    gate: Optional[PfGateConfig] = None


class LearnerExerciseSummary(BaseModel):
    progress_id: Optional[str] = None
    exercise_id: str
    phase: str
    attempts_total: int = 0
    attempts_genuine: int = 0
    explored: bool = False
    latest_signal: Optional[str] = None


class LearnerProgressSummary(BaseModel):
    user_id: str
    display_name: str
    enrolment_id: str
    exercises: List[LearnerExerciseSummary] = []


class GateOverride(BaseModel):
    action: str  # unlock_consolidation | mark_completed | reset_exploring
    reason: str
