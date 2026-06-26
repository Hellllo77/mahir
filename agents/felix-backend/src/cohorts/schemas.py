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
    status: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class InviteLink(BaseModel):
    url: str


class EnrolRequest(BaseModel):
    email: str
    display_name: Optional[str] = None
    password: Optional[str] = None


class EnrolResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    enrolment_id: str
