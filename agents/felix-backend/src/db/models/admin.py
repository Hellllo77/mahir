"""Admin / per-org configuration models."""
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func

from src.db.base import Base
from src.db.uuidv7 import uuid7_str


class OrganisationSettings(Base):
    __tablename__ = "organisation_settings"

    id = Column(String(36), primary_key=True, default=uuid7_str)
    org_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, unique=True)
    resend_api_key = Column(Text, nullable=True)
    updated_by = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
