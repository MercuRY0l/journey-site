import asyncio

from domain.interfaces.user_interface import IUserRepository
from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.interfaces.brute_interface import IBruteService
from domain.interfaces.jwt_interface import IJWTService
from domain.interfaces.hash_pass_interface import IHashPassService
from domain.interfaces.hash_tokens_service import IHashTokenService
from domain.interfaces.log_interface import ILogRepo

from domain.models.user_domain_model import UserDomainModel
from domain.models.auth_tokens_domain_model import AuthTokensDomainModel
from domain.models.log_domain_model import LogDomainModel

from domain.config.config_brute import MAX_ATTEMPTS

from app.dto.register_dto import RegisterDTO
from app.dto.auth_tokens_dto import AuthTokensDTO

from app.exceptions.reg_exceptions import UserAlreadyExists, UsernameAlreadyExists, EmailAlreadyExists

from datetime import datetime, timezone, timedelta

 
class RegisterService:
    
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
    
    async def register(self, reg_dto: RegisterDTO) -> AuthTokensDTO:
         
        if await self.brute_service.is_blocked():
            await self.log_service.create_log(LogDomainModel(event_type="Register", username=None, user_id=None, status="Failed", ip=reg_dto.ip, reason="Регистрация провалена, слишком много попыток регистрации!"))
            raise ValueError("Слишком много попыток, попробуйте позже.")
        
        existing_user = await self.db_user_service.get_user_by_username(reg_dto.username)
        
        if existing_user or await self.db_user_service.get_user_by_email(reg_dto.email):
            attempts = await self.brute_service.record_failed_attempt()
            remaining = max(0, MAX_ATTEMPTS-attempts)
            print("remaining_attempts: ", remaining)
            await self.log_service.create_log(LogDomainModel(event_type="Register", username=None, user_id=None, status="Failed", ip=reg_dto.ip, reason="Регистрация провалена, пользователь уже существует"))
            raise UserAlreadyExists()
        
        hashed_password = self.hash_pass_service.hash(reg_dto.password)   
        
        user = UserDomainModel(
            id=None, 
            username=reg_dto.username,
            email=reg_dto.email,
            password = hashed_password,
            created_at=datetime.now(timezone.utc)
        )
          
        created_user = await self.db_user_service.create_user(user)
        await self.brute_service.reset_attempts()
        
        
        tokens = self.jwt_service.create_jwt_token(created_user.id, created_user.username)
        refresh = self.hash_token_service.hash(tokens['refresh'])
        
        cr_token = AuthTokensDomainModel(
            id=None,
            user_id=created_user.id,
            refresh_token=refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            created_at=datetime.now(timezone.utc)
        )
        
        await self.db_token_service.create_token(cr_token)
        
        await self.log_service.create_log(LogDomainModel(event_type="Register", username=reg_dto.username, user_id=created_user.id, status="Success", ip=reg_dto.ip, reason="Успешная регистрация"))
        
        return AuthTokensDTO(refresh_token=tokens['refresh'], access_token=tokens['access'])