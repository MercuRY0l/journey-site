
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserDomainModel:
    id:int
    username:str
    password:str
    email:str
    created_at:datetime