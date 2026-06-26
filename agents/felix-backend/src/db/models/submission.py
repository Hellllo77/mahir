"""Submission & EvaluationResult models (ADR-003, data-model §4)."""
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from src.db.base import AuditMixin, Base


class SubmissionStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    evaluated = "evaluated"
    failed = "failed"


class Submission(AuditMixin, Base):
    __tablename__ = "submissions"

    exercise_progress_id = Column(String(36), ForeignKey("exercise_progress.id"), nullable=False)
    enrolment_id = Column(String(36), ForeignKey("enrolments.id"), nullable=False)
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    attempt_number = Column(Integer, nullable=False)
    payload = Column(Text, nullable=False)  # JSONB; schema_version required
    artifact_refs = Column(Text, nullable=True)  # JSONB nullable
    status = Column(Enum(SubmissionStatus, native_enum=False), nullable=False, default=SubmissionStatus.queued)
    idempotency_key = Column(Text, unique=True, nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=False)

    enrolment = relationship("Enrolment", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")
    result = relationship("EvaluationResult", back_populates="submission", uselist=False, lazy="select")


class PFSignal(str, enum.Enum):
    productive = "productive"
    low_effort = "low_effort"
    off_task = "off_task"


class EvaluationResult(AuditMixin, Base):
    __tablename__ = "evaluation_results"

    submission_id = Column(String(36), ForeignKey("submissions.id"), unique=True, nullable=False)
    schema_version = Column(Text, nullable=False, default="1.0")
    ran = Column(Boolean, nullable=False)
    scenario_results = Column(Text, nullable=True)  # JSONB [{scenario_id, passed, detail}]
    rubric_scores = Column(Text, nullable=True)   # JSONB [{criterion_id, met, score, confidence, severity, evidence}]
    overall_score = Column(Numeric, nullable=False)
    productive_failure_signal = Column(Enum(PFSignal, native_enum=False), nullable=False)
    detected_approach = Column(Text, nullable=True)
    confidence = Column(Numeric, nullable=True)
    passed = Column(Boolean, nullable=False)
    feedback_markdown = Column(Text, nullable=True)
    feedback_artifact_ref = Column(Text, nullable=True)  # JSONB nullable
    judge_model = Column(Text, nullable=False)
    judge_escalated = Column(Boolean, nullable=False, default=False)
    usage_input_tokens = Column(Integer, nullable=True)
    usage_output_tokens = Column(Integer, nullable=True)
    usage_cache_read_tokens = Column(Integer, nullable=True)
    cost_micro_usd = Column(Integer, nullable=True)
    evaluated_at = Column(DateTime(timezone=True), nullable=False)

    submission = relationship("Submission", back_populates="result")
