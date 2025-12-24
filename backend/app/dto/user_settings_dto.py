from pydantic import BaseModel, StringConstraints

from typing import Optional
from typing_extensions import Annotated


Username = Annotated[
    str,
    StringConstraints(min_length=5, max_length=50)
]

Email = Annotated[
    str,
    StringConstraints(max_length=255)
]

Password = Annotated[
    str,
    StringConstraints(min_length=8, max_length=255)
]

class ChangeUsername(BaseModel):
    new_username: Username
    ip: Optional[str] = None
    
class ChangeEmail(BaseModel):
    new_email: Email
    ip: Optional[str] = None
    
class ChangePassword(BaseModel):
    old_password: str
    new_password: Password
    ip: Optional[str] = None
