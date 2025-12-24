



from pydantic import BaseModel, StringConstraints

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



class RegisterDTO(BaseModel):
    
    username : Username
    email : Email
    password : Password
    password_repeat : Password
    
