from ..models.auth_tokens_domain_model import AuthTokensDomainModel
from ..interfaces.auth_tokens_interface import IAuthTokensRepository
from ..interfaces.hash_interface import IHashService
class AuthTokensModelService:
    
    def __init__(self, repo: IAuthTokensRepository, hash_service:  IHashService):
        self.repo = repo
        self.hash_service = hash_service
    
    def create_token(self, user_id, refresh_token, expires_at):
        token = AuthTokensDomainModel(user_id=user_id, refresh_token=refresh_token, expires_at=expires_at)
        self.repo.create_token(token=token)
        return token
        
    def delete_refresh_token(self, user_id: int, token: str):
        tokens = self.repo.get_all_refresh_hashes(user_id)
        for token_hash, token_id in tokens:
            if self.hash_service.check(token, token_hash):
                self.repo.delete_by_id(token_id)
                return True
        return False

    def find_token_by_userid(self,user_id):
        return self.repo.find_token_by_userid(user_id=user_id)
            
    
    def find_token_by_refresh(self, refresh_token):       
        return self.repo.find_token_by_refresh(refresh_token=refresh_token)
            
         