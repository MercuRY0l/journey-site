

from pydantic import BaseModel

class AuthTokensDTO(BaseModel):
    refresh_token: str
    access_token: str