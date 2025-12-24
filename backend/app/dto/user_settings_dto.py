from pydantic import BaseModel
from typing import Optional

class ChangeUsername(BaseModel):
    new_username: str
    ip: Optional[str] = None
    
class ChangeEmail(BaseModel):
    new_email: str
    ip: Optional[str] = None
    
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    ip: Optional[str] = None
