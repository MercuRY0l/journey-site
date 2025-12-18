from dataclasses import dataclass
from typing import Optional
@dataclass
class LogoutDTO:
    refresh_token : str
    ip: Optional[str]