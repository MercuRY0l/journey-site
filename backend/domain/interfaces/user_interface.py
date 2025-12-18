

from abc import abstractmethod, ABC
from domain.models.user_domain_model import UserDomainModel

class IUserRepository(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    async def create_user(self, user: UserDomainModel) -> UserDomainModel:
        pass
    
    @abstractmethod
    async def delete_user(self):
        pass
    
    @abstractmethod
    async def get_user_by_username(self, username : str) -> str:
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email : str) -> str:
        pass
    
    @abstractmethod
    async def get_user_by_user_id(self, user_id: int) -> str:
        pass
