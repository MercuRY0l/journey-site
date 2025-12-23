
from ..interfaces.blacklist_interface import IBlacklistRepository
from domain.models.blacklist_domain_model import BlacklistDomainModel

class BlackListTokensModelService:
    
    def __init__(self, repo: IBlacklistRepository):
        self.repo = repo
    
    async def create_blacklisted(self , blacklisted: BlacklistDomainModel):
        return await self.repo.create_blacklisted(blacklisted=blacklisted)
        
 
    async def delete_blacklisted_by_token(self, token):
        await self.repo.delete_blacklisted(token=token)

    async def find_blacklisted_by_token(self, token):
        return await self.repo.find_blacklisted_by_token(token=token)