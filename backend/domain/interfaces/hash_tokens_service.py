
from abc import ABC, abstractmethod

class IHashTokenService(ABC):
    
    @abstractmethod
    def hash(self, token : str):
        pass