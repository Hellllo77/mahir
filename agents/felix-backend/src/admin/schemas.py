from typing import Optional
from pydantic import BaseModel, field_validator


class SettingsOut(BaseModel):
    resend_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    preferred_model: Optional[str] = None


class SettingsUpdate(BaseModel):
    resend_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    preferred_model: Optional[str] = None

    @field_validator("resend_api_key")
    @classmethod
    def resend_key_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("resend_api_key cannot be empty string")
        return v

    @field_validator("openrouter_api_key")
    @classmethod
    def openrouter_key_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("openrouter_api_key cannot be empty string")
        return v
