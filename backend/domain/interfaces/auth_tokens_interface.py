
from abc import ABC, abstractmethod
from domain.models.auth_tokens_domain_model import AuthTokensDomainModel

class IAuthTokensRepository(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    async def create_token(self, token: AuthTokensDomainModel) -> AuthTokensDomainModel:
        pass
     
    @abstractmethod
    async def get_all_refresh_hashes(self,  user_id: int) -> str:
        pass
    
    @abstractmethod
    async def delete_refresh_token(self, user_id: int , hashed_token : str) -> int:
        pass    
    
    @abstractmethod
    async def delete_refresh_by_id(self, token_id: int):
        pass
    
    @abstractmethod
    async def find_token_by_userid(self, user_id: int) -> str:
        pass
    
    @abstractmethod
    async def find_token_by_refresh(self, refresh_token: str) -> str:
        pass
     