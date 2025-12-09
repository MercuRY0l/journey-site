
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BlacklistDomainModel():
    id:int
    token:str
    token_type:str
    user_id:int
    reason:str
    created_at:datetime
    expires_at:datetime
    