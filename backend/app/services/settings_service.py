
from infrastructure.services.hash_pass_service import HashPassService
from infrastructure.services.brute_protection_service import BruteService
from infrastructure.repositories.user_repo import IUserRepository

from domain.services.log_service import LogService
from domain.models.log_domain_model import LogDomainModel

from app.dto.user_settings_dto import ChangeUsername, ChangeEmail, ChangePassword
class SettingsService:
    def __init__(self, 
                 db_user_repo : IUserRepository, 
                 hash_pass_service : HashPassService, 
                 log_service: LogService, 
                 brute_service : BruteService):
        
        self.db_user_repo = db_user_repo
        self.hash_pass_service = hash_pass_service
        self.log_service = log_service
        self.brute_service = brute_service
        
    async def change_username(self, username_dto : ChangeUsername, user_id : int, new_username: str):        
        try:
            await self.db_user_repo.change_username(user_id=user_id, new_username=new_username)
            await self.log_service.create_log(LogDomainModel(event_type="ChangeUsername", 
                                                         username=new_username, 
                                                         user_id=user_id, 
                                                         status="success", 
                                                         ip=username_dto.ip,
                                                         reason="Успешная смена username"))
        except Exception as e:
            
            await self.log_service.create_log(LogDomainModel(event_type="ChangeUsername", 
                                                         username=new_username, 
                                                         user_id=user_id, 
                                                         status="failed", 
                                                         ip=username_dto.ip,
                                                         reason="Не удачная смена username"))

            raise e
        
    async def change_email(self, email_dto : ChangeEmail, user_id : int, new_email: str):
        try:
            await self.db_user_repo.change_email(user_id=user_id, new_email=new_email)
            await self.log_service.create_log(LogDomainModel(event_type="ChangeEmail", 
                                                         username=None, 
                                                         user_id=user_id, 
                                                         status="success", 
                                                         ip=email_dto.ip,
                                                         reason="Успешная смена почты"))

        except Exception as e:
            
            await self.log_service.create_log(LogDomainModel(event_type="ChangeEmail", 
                                                         username=None, 
                                                         user_id=user_id, 
                                                         status="failed", 
                                                         ip=email_dto.ip,
                                                         reason="Не удачная смена почты"))
            raise e
            
    async def change_password(self, pass_dto: ChangePassword, user_id : int, new_password : str):
        
        user = await self.db_user_repo.get_user_by_user_id(user_id=user_id)
        
        # if not user: #TODO доделать проверку
        #     raise UserNotFound()
        
        if not self.hash_pass_service.check(pass_dto.old_password, user.password):
            raise ValueError("Пароли не совпадают!")
        
        try:
            new_password = self.hash_pass_service.hash(new_password)
            
            await self.db_user_repo.change_password(user_id=user_id, new_password=new_password)
            
            await self.log_service.create_log(LogDomainModel(event_type="ChangePassword", 
                                                        username=None, 
                                                        user_id=user_id, 
                                                        status="success", 
                                                        ip=pass_dto.ip,
                                                        reason="Успешная смена пароля"))
            

        except Exception as e:
            await self.log_service.create_log(LogDomainModel(event_type="ChangePassword", 
                                                         username=None, 
                                                         user_id=user_id, 
                                                         status="failed", 
                                                         ip=pass_dto.ip,
                                                         reason="Не удачная смена пароля"))
            
            raise e