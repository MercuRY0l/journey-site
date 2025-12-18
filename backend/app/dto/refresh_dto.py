from dataclasses import dataclass
from typing import Optional

@dataclass
class RefreshDTO:
    refresh_token : str
    access_token : str
    ip: Optional[str]