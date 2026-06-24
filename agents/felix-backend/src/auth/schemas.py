from pydantic import BaseModel, EmailStr
from typing import List


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class EnrolmentRef(BaseModel):
    id: str
    cohort_id: str
    role: str
    status: str


class Me(BaseModel):
    id: str
    email: str
    display_name: str
    organization_id: str
    global_role: str
    enrolments: List[EnrolmentRef]
