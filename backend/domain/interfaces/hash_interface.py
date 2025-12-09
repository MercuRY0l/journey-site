
from abc import ABC, abstractmethod

class IHashService(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def hash(self, obj) -> str:
        pass
    
    @abstractmethod
    def check(self, plaintext: str, hashed: str) -> bool:
        pass