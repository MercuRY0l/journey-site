import asyncio

from datetime import datetime, timezone, timedelta

from domain.interfaces.user_interface import IUserRepository
from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.interfaces.brute_interface import IBruteService
from domain.interfaces.jwt_interface import IJWTService
from domain.interfaces.hash_pass_interface import IHashPassService
from domain.interfaces.hash_tokens_service import IHashTokenService
from domain.interfaces.log_interface import ILogRepo

from domain.config.config_brute import MAX_ATTEMPTS

from domain.models.auth_tokens_domain_model import AuthTokensDomainModel
from domain.models.log_domain_model import LogDomainModel

from app.dto.login_dto import LoginDTO
from app.dto.auth_tokens_dto import AuthTokensDTO
from app.exceptions.login_exceptions import UserIsNotExists, WrongPassword



class LoginService:
    
    def __init__(self, 
                 db_user_service: IUserRepository, 
                 db_token_service:IAuthTokensRepository, 
                 jwt_service: IJWTService, 
                 brute_service : IBruteService,
                 hash_pass_service: IHashPassService, 
                 hash_token_service : IHashTokenService,
                 log_service : ILogRepo):
        
        self.db_user_service = db_user_service
        self.db_token_service = db_token_service
        self.jwt_service = jwt_service
        self.brute_service = brute_service
        self.hash_pass_service = hash_pass_service
        self.hash_token_service = hash_token_service
        self.log_service = log_service
        
    async def login(self, login_dto: LoginDTO):
    
        if await self.brute_service.is_blocked():
            await self.log_service.create_log(LogDomainModel(event_type="Login", username=login_dto.username , user_id=None, status="Failed", ip=login_dto.ip, reason="Неудачная попытка входа, IP заблокирован!"))
            raise ValueError("Слишком много попыток, попробуйте позже.")
        
        user = await self.db_user_service.get_user_by_username(login_dto.username)
        
        if not user:
            attemps = await self.brute_service.record_failed_attempt()
            remaining = max(0, MAX_ATTEMPTS-attemps)    
            print("Оставшиеся попытки:", remaining)
            await self.log_service.create_log(LogDomainModel(event_type="Login", username=login_dto.username ,user_id=None, status="Failed", ip=login_dto.ip, reason="Неудачная попытка входа, пользователя не существует!"))
            raise UserIsNotExists()
        
        if not self.hash_pass_service.check(login_dto.password, user.password):
            attemps = await self.brute_service.record_failed_attempt()
            remaining = max(0, MAX_ATTEMPTS-attemps)    
            print("Оставшиеся попытки:", remaining)
            await self.log_service.create_log(LogDomainModel(event_type="Login", username=login_dto.username ,user_id=user.id, status="Failed", ip=login_dto.ip, reason="Неудачная попытка входа, неверный пароль!"))
            raise WrongPassword()
        
        tokens = self.jwt_service.create_jwt_token(user.id, user.username)
        new_refresh_token = self.hash_token_service.hash(tokens['refresh'])
        
        cr_token = AuthTokensDomainModel(
            id=None,
            user_id=user.id,
            refresh_token=new_refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            created_at=datetime.now(timezone.utc)
            
        )
        
        await self.brute_service.reset_attempts()
        await self.db_token_service.create_token(cr_token)
        
        await self.log_service.create_log(LogDomainModel(event_type="Login", username=login_dto.username, user_id=user.id, status="Success", ip=login_dto.ip, reason="Пользователь успешно вошел!"))
        
        return AuthTokensDTO(refresh_token=tokens['refresh'], access_token=tokens['access'])
        
        
    
                    
                