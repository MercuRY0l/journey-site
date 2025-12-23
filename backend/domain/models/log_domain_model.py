
from dataclasses import dataclass

@dataclass
class LogDomainModel:
    event_type:str
    username:str
    user_id:int
    status:str
    ip:str
    reason:str  