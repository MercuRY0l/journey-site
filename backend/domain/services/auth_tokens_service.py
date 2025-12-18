from ..models.auth_tokens_domain_model import AuthTokensDomainModel
from ..interfaces.auth_tokens_interface import IAuthTokensRepository

class AuthTokensModelService:
    
    def __init__(self, repo: IAuthTokensRepository):
        self.repo = repo
    
    async def create_token(self, token: AuthTokensDomainModel):
        return await self.repo.create_token(token=token)
        
    async def delete_refresh_token(self, user_id: int, hashed_token: str) -> int:
        return await self.repo.delete_refresh_token(user_id=user_id, token=hashed_token)
        
    async def find_token_by_userid(self,user_id): 
        return await self.repo.find_token_by_userid(user_id=user_id)
            
    async def find_token_by_refresh(self, refresh_token):       
        return await self.repo.find_token_by_refresh(refresh_token=refresh_token)
            
          