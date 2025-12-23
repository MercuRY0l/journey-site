

from pydantic import BaseModel
from typing import Optional

class SettingsModel(BaseModel):
    username: str | Optional[str]
    email: str | Optional[str]
    password1 : str | Optional[str]
    password2 : str | Optional[str]
    password2_repeat : str | Optional[str]