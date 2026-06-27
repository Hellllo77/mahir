from typing import Optional
from pydantic import BaseModel


class SettingsOut(BaseModel):
    resend_api_key: Optional[str] = None


class SettingsUpdate(BaseModel):
    resend_api_key: str
