"""Progress store — server-authoritative PF phase state (ADR-004, data-model §3)."""
import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from src.db.base import AuditMixin, Base


class ExercisePhase(str, enum.Enum):
    not_started = "not_started"
    exploring = "exploring"
    consolidation_unlocked = "consolidation_unlocked"
    completed = "completed"


class ExerciseProgress(AuditMixin, Base):
    """Per (learner, exercise) PF phase state. Single source of truth per ADR-004."""

    __tablename__ = "exercise_progress"

    enrolment_id = Column(String(36), ForeignKey("enrolments.id"), nullable=False)
    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    phase = Column(Enum(ExercisePhase, native_enum=False), nullable=False, default=ExercisePhase.not_started)
    attempts_total = Column(Integer, nullable=False, default=0)
    attempts_genuine = Column(Integer, nullable=False, default=0)
    distinct_approaches = Column(Integer, nullable=False, default=0)
    exploration_seconds = Column(Integer, nullable=False, default=0)
    explored = Column(Boolean, nullable=False, default=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    mastery_score = Column(Numeric, nullable=True)
    facilitator_override = Column(Text, nullable=True)  # JSONB — audited manual gate override

    __table_args__ = (
        UniqueConstraint("enrolment_id", "exercise_id", name="uq_progress_enrolment_exercise"),
    )

    enrolment = relationship("Enrolment", back_populates="progress_records")
    exercise = relationship("Exercise", back_populates="progress_records")
