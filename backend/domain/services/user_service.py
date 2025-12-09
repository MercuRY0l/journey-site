

from domain.models.user_domain_model import UserDomainModel
from domain.interfaces.user_interface import IUserRepository
class UserModelService:

    def __init__(self, repository: IUserRepository):
        self.repo = repository

    def create_user(self, username, email, password):
        
        user = UserDomainModel(username = username, email = email, password = password)
        self.repo.create_user(user=user)
        self.repo.commit()
        return user
       
   
    def delete_user(self, username : str): 
        self.repo.delete_user(username=username)
        self.repo.commit()
    
            
    def get_user_by_username(self,username : str) -> str:
        return self.repo.get_user_by_username(username=username)
        
    def get_user_by_email(self, email : str) -> str:
       return self.repo.get_user_by_email(email=email)
    
    def get_user_by_user_id(self, user_id : int) -> str:
        return self.repo.get_user_by_user_id(user_id=user_id)
