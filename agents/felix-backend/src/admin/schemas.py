from typing import Optional
from pydantic import BaseModel, field_validator


class SettingsOut(BaseModel):
    resend_api_key: Optional[str] = None


class SettingsUpdate(BaseModel):
    resend_api_key: Optional[str]

    @field_validator("resend_api_key")
    @classmethod
    def key_must_not_be_empty(cls, v: Optional[str]) -> str:
        if not v or not v.strip():
            raise ValueError("resend_api_key cannot be empty")
        return v
