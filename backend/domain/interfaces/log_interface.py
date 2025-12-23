
from abc import ABC, abstractmethod

from domain.models.log_domain_model import LogDomainModel

class ILogRepo(ABC):
    
    @abstractmethod
    async def create_log(self, log: LogDomainModel): 
        pass
    
    @abstractmethod
    async def find_log(self, user_id : int):
        pass
    
    @abstractmethod
    async def delete_log(self, user_id : int):
        pass 