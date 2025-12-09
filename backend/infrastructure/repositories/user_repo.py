from domain.interfaces.user_interface import IUserRepository
from domain.models.user_domain_model import UserDomainModel

from sqlalchemy import delete

from infrastructure.config.connector import SessionLocal

class UserRepository(IUserRepository):
    def __init__(self):
        self.session = SessionLocal()
        
    def create_user(self, user: UserDomainModel) -> UserDomainModel:
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.session.close()
        
        return user
        
    def delete_user(self, username : str):
        stmt = delete(UserDomainModel).where(UserDomainModel.username == username)
        return self.session.execute(stmt)
    
    def get_user_by_username(self, username : str) -> str:
        return self.session.query(UserDomainModel).filter(UserDomainModel.username == username).first()
    
    def get_user_by_email(self, email: str) -> str:
        return self.session.query(UserDomainModel).filter(UserDomainModel.email == email).first()
    
    def get_user_by_user_id(self, user_id: int) -> str:
        return self.session.query(UserDomainModel).filter(UserDomainModel.id == user_id).first()
    
    def close(self): 
        self.session.close()
        
    def commit(self):
        self.session.commit()
        
    def rollback(self):
        self.session.rollback()