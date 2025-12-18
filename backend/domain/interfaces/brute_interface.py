

from abc import ABC, abstractmethod

class IBruteService(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_client_ip(self, request):
        pass
    
    @abstractmethod
    def _attempts_cache_key(self):
        pass
    
    @abstractmethod
    def _blocked_cache_key(self): 
        pass
    
    @abstractmethod
    async def is_blocked(self):
        pass
    
    @abstractmethod
    async def record_failed_attempt(self):
        pass
    
    @abstractmethod
    async def reset_attempts(self):
        pass
