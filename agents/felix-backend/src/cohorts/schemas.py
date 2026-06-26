from datetime import date
from typing import Optional

from pydantic import BaseModel


class CohortSummary(BaseModel):
    id: str
    name: str
    status: str
    learner_count: int


class CohortCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class CohortDetail(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: str
    starts_on: Optional[str]
    enrollment_count: int = 0


class CohortUpdate(BaseModel):
    status: str


class InviteLink(BaseModel):
    url: str
