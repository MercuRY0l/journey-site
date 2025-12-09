





from dataclasses import dataclass

@dataclass
class RegisterDTO:
    def __init__(self, username: str, password : str, email:str):
        self.username = username
        self.password = password
        self.email = email
        
