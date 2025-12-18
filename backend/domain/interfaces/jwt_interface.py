
from abc import ABC, abstractmethod

class IJWTService(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def create_jwt_token(self, user_id :int, username : str):
        pass
    
    @abstractmethod
    def decode_jwt_token(self, token:str):
        pass