

from abc import abstractmethod, ABC
from domain.models.user_domain_model import UserDomainModel

class IUserRepository(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def create_user(self, user: UserDomainModel) -> UserDomainModel:
        pass
    
    @abstractmethod
    def delete_user(self):
        pass
    
    @abstractmethod
    def get_user_by_username(self, username : str) -> str:
        pass
    
    @abstractmethod
    def get_user_by_email(self, email : str) -> str:
        pass
    
    @abstractmethod
    def get_user_by_user_id(self, user_id: int) -> str:
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass