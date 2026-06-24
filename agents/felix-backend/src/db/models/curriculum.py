"""Curriculum models (ADR-001, data-model §2)."""
import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from src.db.base import AuditMixin, Base


class CurriculumEdition(str, enum.Enum):
    co_worker = "co_worker"
    co_founder = "co_founder"


class CurriculumStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Curriculum(AuditMixin, Base):
    __tablename__ = "curricula"

    edition = Column(Enum(CurriculumEdition), nullable=False)
    title = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    status = Column(Enum(CurriculumStatus), nullable=False, default=CurriculumStatus.draft)

    modules = relationship("Module", back_populates="curriculum", lazy="select", order_by="Module.sequence_index")


class Module(AuditMixin, Base):
    __tablename__ = "modules"

    curriculum_id = Column(String(36), ForeignKey("curricula.id"), nullable=False)
    title = Column(Text, nullable=False)
    sequence_index = Column(Integer, nullable=False)
    summary_markdown = Column(Text, nullable=True)

    curriculum = relationship("Curriculum", back_populates="modules")
    exercises = relationship("Exercise", back_populates="module", lazy="select", order_by="Exercise.sequence_index")


class Exercise(AuditMixin, Base):
    """PF unit — carries gate hyperparameters per ADR-004."""

    __tablename__ = "exercises"

    module_id = Column(String(36), ForeignKey("modules.id"), nullable=False)
    title = Column(Text, nullable=False)
    sequence_index = Column(Integer, nullable=False)
    prompt_markdown = Column(Text, nullable=False)
    build_spec = Column(Text, nullable=False)  # JSONB; schema_version required
    prerequisite_exercise_ids = Column(Text, nullable=True)  # JSONB array of UUIDs
    # PF gate hyperparameters (ADR-004)
    min_attempts = Column(Integer, nullable=False, default=2)
    min_distinct_approaches = Column(Integer, nullable=False, default=2)
    min_exploration_seconds = Column(Integer, nullable=False, default=300)
    allow_fast_unlock = Column(Boolean, nullable=False, default=True)

    module = relationship("Module", back_populates="exercises")
    scenarios = relationship("Scenario", back_populates="exercise", lazy="select")
    rubric_criteria = relationship("RubricCriterion", back_populates="exercise", lazy="select")
    approach_taxonomy = relationship("ApproachTaxonomy", back_populates="exercise", lazy="select")
    consolidation = relationship("ConsolidationContent", back_populates="exercise", uselist=False, lazy="select")
    progress_records = relationship("ExerciseProgress", back_populates="exercise", lazy="select")
    submissions = relationship("Submission", back_populates="exercise", lazy="select")


class Scenario(AuditMixin, Base):
    __tablename__ = "scenarios"

    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    name = Column(Text, nullable=False)
    input_payload = Column(Text, nullable=False)  # JSONB; schema_version required
    assertions = Column(Text, nullable=False)  # JSONB; schema_version required
    weight = Column(Numeric, nullable=False, default=1.0)

    exercise = relationship("Exercise", back_populates="scenarios")


class RubricCriterion(AuditMixin, Base):
    __tablename__ = "rubric_criteria"

    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    code = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Numeric, nullable=False, default=1.0)
    guidance_markdown = Column(Text, nullable=True)

    exercise = relationship("Exercise", back_populates="rubric_criteria")


class ApproachTaxonomy(AuditMixin, Base):
    """Recognised solution approaches; judge tags submissions with one of these codes."""

    __tablename__ = "approach_taxonomies"

    exercise_id = Column(String(36), ForeignKey("exercises.id"), nullable=False)
    code = Column(Text, nullable=False)  # e.g. approach.single-prompt-no-tools
    label = Column(Text, nullable=False)
    is_canonical = Column(Boolean, nullable=False, default=False)

    exercise = relationship("Exercise", back_populates="approach_taxonomy")


class ConsolidationContent(AuditMixin, Base):
    """Reference solution — revealed ONLY after PF gate passes (ADR-004 invariant 1)."""

    __tablename__ = "consolidation_contents"

    exercise_id = Column(String(36), ForeignKey("exercises.id"), unique=True, nullable=False)
    body_markdown = Column(Text, nullable=False)
    reference_build = Column(Text, nullable=True)  # JSONB; schema_version required
    check_questions = Column(Text, nullable=True)  # JSONB nullable

    exercise = relationship("Exercise", back_populates="consolidation")
