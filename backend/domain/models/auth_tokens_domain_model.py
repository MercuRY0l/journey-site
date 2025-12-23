

from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuthTokensDomainModel:
    id:int
    user_id:int
    refresh_token:str
    expires_at:datetime
    created_at:datetime