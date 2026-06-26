"""Identity & Org models — auth module (ADR-001, data-model §1)."""
import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from src.db.base import AuditMixin, Base


class OrgEdition(str, enum.Enum):
    co_worker = "co_worker"
    co_founder = "co_founder"


class OrgStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"


class Organization(AuditMixin, Base):
    __tablename__ = "organizations"

    name = Column(Text, nullable=False)
    slug = Column(Text, unique=True, nullable=False)
    edition = Column(Enum(OrgEdition, native_enum=False), nullable=False, default=OrgEdition.co_worker)
    region = Column(Text, nullable=False)
    sso_config = Column("sso_config", Text, nullable=True)  # JSONB stored as text in ORM; use JSON type in migration
    status = Column(Enum(OrgStatus, native_enum=False), nullable=False, default=OrgStatus.active)

    users = relationship("User", back_populates="organization", lazy="select")
    cohorts = relationship("Cohort", back_populates="organization", lazy="select")


class UserAuthProvider(str, enum.Enum):
    oidc = "oidc"
    local = "local"


class UserGlobalRole(str, enum.Enum):
    learner = "learner"
    facilitator = "facilitator"
    org_admin = "org_admin"
    super_admin = "super_admin"


class UserStatus(str, enum.Enum):
    invited = "invited"
    active = "active"
    deactivated = "deactivated"


class User(AuditMixin, Base):
    __tablename__ = "users"

    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    email = Column(Text, nullable=False)  # citext — case-insensitive handled at DB level
    display_name = Column(Text, nullable=False)
    auth_provider = Column(Enum(UserAuthProvider, native_enum=False), nullable=False)
    external_subject = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=True)
    global_role = Column(Enum(UserGlobalRole, native_enum=False), nullable=False, default=UserGlobalRole.learner)
    status = Column(Enum(UserStatus, native_enum=False), nullable=False, default=UserStatus.invited)

    __table_args__ = (UniqueConstraint("organization_id", "email", name="uq_user_org_email"),)

    organization = relationship("Organization", back_populates="users")
    enrolments = relationship("Enrolment", back_populates="user", lazy="select")


class CohortStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    running = "running"
    completed = "completed"
    archived = "archived"


class Cohort(AuditMixin, Base):
    __tablename__ = "cohorts"

    organization_id = Column(String(36), ForeignKey("organizations.id"), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    curriculum_id = Column(String(36), ForeignKey("curricula.id"), nullable=True)
    starts_on = Column(Text, nullable=True)  # date stored as ISO string
    ends_on = Column(Text, nullable=True)
    status = Column(Enum(CohortStatus, native_enum=False), nullable=False, default=CohortStatus.draft)

    organization = relationship("Organization", back_populates="cohorts")
    enrolments = relationship("Enrolment", back_populates="cohort", lazy="select")


class EnrolmentRole(str, enum.Enum):
    learner = "learner"
    facilitator = "facilitator"


class EnrolmentStatus(str, enum.Enum):
    active = "active"
    withdrawn = "withdrawn"
    completed = "completed"


class Enrolment(AuditMixin, Base):
    __tablename__ = "enrolments"

    cohort_id = Column(String(36), ForeignKey("cohorts.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    role = Column(Enum(EnrolmentRole, native_enum=False), nullable=False, default=EnrolmentRole.learner)
    status = Column(Enum(EnrolmentStatus, native_enum=False), nullable=False, default=EnrolmentStatus.active)

    __table_args__ = (UniqueConstraint("cohort_id", "user_id", name="uq_enrolment_cohort_user"),)

    cohort = relationship("Cohort", back_populates="enrolments")
    user = relationship("User", back_populates="enrolments")
    progress_records = relationship("ExerciseProgress", back_populates="enrolment", lazy="select")
    submissions = relationship("Submission", back_populates="enrolment", lazy="select")
