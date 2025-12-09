
from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.models.auth_tokens_domain_model import AuthTokensDomainModel

from infrastructure.config.connector import SessionLocal

from sqlalchemy import delete


class AuthTokensRepository(IAuthTokensRepository):
    
    def __init__(self):
        self.session = SessionLocal()
        
    def create_token(self, token: AuthTokensDomainModel) -> AuthTokensDomainModel:
        
        self.session.add(token)
        self.session.commit()
        self.session.refresh(token)
        self.session.close()
        
        return token
    
    def delete_refresh_token(self, user_id : int, token: str):
        pass
    
    def delete_refresh_by_id(self, id_token : int):
        stmt = delete(AuthTokensDomainModel).where(AuthTokensDomainModel.id == id_token)
        self.session.execute(stmt)
        self.session.commit()
        
    def get_all_refresh_hashes(self, user_id: int) -> str:
        query = self.session.query(
            AuthTokensDomainModel.refresh_token,
            AuthTokensDomainModel.id
        ).filter(AuthTokensDomainModel.user_id == user_id)

        return query.all()    
    
    def find_token_by_userid(self,user_id : int) -> str:
        
        return self.session.query(AuthTokensDomainModel).filter(AuthTokensDomainModel.user_id == user_id).first()
            
        
    def find_token_by_refresh(self, refresh_token : str) -> str:    
        
        return self.session.query(AuthTokensDomainModel).filter(AuthTokensDomainModel.refresh_token == refresh_token).first()
        
    def close(self):
        self.session.close()
         