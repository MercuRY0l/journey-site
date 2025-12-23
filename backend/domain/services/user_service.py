

from domain.models.user_domain_model import UserDomainModel
from domain.interfaces.user_interface import IUserRepository
class UserModelService:

    def __init__(self, repository: IUserRepository):
        self.repo = repository

    async def create_user(self, user: UserDomainModel):
        return await self.repo.create_user(user=user)
       
    async def delete_user(self, username : str): 
        await self.repo.delete_user(username=username)
            
    async def get_user_by_username(self,username : str) -> str:
        return await self.repo.get_user_by_username(username=username)
        
    async def get_user_by_email(self, email : str) -> str:
        return await self.repo.get_user_by_email(email=email)
    
    async def get_user_by_user_id(self, user_id : int) -> str:
        return await self.repo.get_user_by_user_id(user_id=user_id)
