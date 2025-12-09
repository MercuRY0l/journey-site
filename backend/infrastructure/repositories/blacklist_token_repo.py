
from domain.interfaces.blacklisted_interface import IBlacklistRepository
from domain.models.blacklist_domain_model import BlacklistDomainModel

from infrastructure.config.connector import SessionLocal

from sqlalchemy import delete

class BlackListTokenRepository(IBlacklistRepository):
    
    def __init__(self):
        self.session = SessionLocal()
        
        
    def create_blacklisted(self , blacklisted: BlacklistDomainModel) -> BlacklistDomainModel:
        
        self.session.add(blacklisted)
        self.session.commit()
        self.session.refresh(blacklisted)
        self.session.close()
         
        return blacklisted
    
    
    def delete_blacklisted_by_token(self, token : str):
        
        stmt = delete(BlacklistDomainModel).where(BlacklistDomainModel.token == token)
        self.session.execute(stmt)
        self.session.commit()
        
    
    def find_blacklisted_by_token(self, token : str) -> str:
        
        return self.session.query(BlacklistDomainModel).filter(BlacklistDomainModel.token == token).first()

    def close(self):
        self.session.close()
        