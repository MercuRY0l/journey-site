from abc import ABC, abstractmethod
from domain.models.blacklist_domain_model import BlacklistDomainModel
class IBlacklistRepository(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    async def create_blacklisted(self, blacklisted_token: BlacklistDomainModel) -> BlacklistDomainModel:
        pass
    
    @abstractmethod
    async def delete_blacklisted_by_token(self, token: str):
        pass
    
    @abstractmethod
    async def find_blacklisted_by_token(self, token: str) -> str:
        pass