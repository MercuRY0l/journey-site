
from domain.interfaces.blacklisted_interface import IBlacklistRepository
from domain.models.blacklist_domain_model import BlacklistDomainModel

class BlackListTokensModelService:
    
    def __init__(self, repo: IBlacklistRepository):
        self.repo = repo
    
    def create_blacklisted(self , token, token_type, user_id, reason, expires_at):

        blacklisted = BlacklistDomainModel(token=token, token_type=token_type, user_id=user_id, reason=reason, expires_at=expires_at)
        self.repo.create_blacklisted(blacklisted=blacklisted)
        return blacklisted
 
    def delete_blacklisted_by_token(self, token):
        self.repo.delete_blacklisted(token=token)

    def find_blacklisted_by_token(self, token):
        return self.repo.find_blacklisted_by_token(token=token)
    
    