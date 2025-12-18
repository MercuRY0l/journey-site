

from domain.interfaces.log_interface import ILogRepo
from domain.models.log_domain_model import LogDomainModel

class LogService:
    def __init__(self, repo : ILogRepo):
        self.repo = repo
        
    async def create_log(self, log: LogDomainModel):
        return await self.repo.create_log(log)
    
    async def delete_log(self, user_id):
        await self.repo.delete_log(user_id=user_id)
    
    async def find_log(self, user_id):
        return await self.repo.find_log(user_id=user_id) 