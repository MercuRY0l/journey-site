






from dataclasses import dataclass

@dataclass
class LoginDTO:
    def __init__(self, username: str, password : str):
        self.username = username
        self.password = password
