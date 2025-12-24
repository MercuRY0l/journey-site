

from pydantic import BaseModel,StringConstraints

from typing_extensions import Annotated

Username = Annotated[
    str,
    StringConstraints(min_length=5, max_length=50)
]


Password = Annotated[
    str,
    StringConstraints(min_length=8, max_length=255)
]

class LoginDTO(BaseModel):
    
    username: Username
    password: Password
        
