
from datetime import datetime, timezone, timedelta

from domain.interfaces.user_interface import IUserRepository
from domain.interfaces.blacklist_interface import IBlacklistRepository
from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.interfaces.jwt_interface import IJWTService
from domain.interfaces.hash_tokens_service import IHashTokenService
from domain.interfaces.log_interface import ILogRepo
from domain.interfaces.brute_interface import IBruteService


from domain.models.auth_tokens_domain_model import AuthTokensDomainModel
from domain.models.blacklist_domain_model import BlacklistDomainModel

from app.dto.refresh_dto import RefreshDTO

from app.exceptions.refresh_exceptions import TokenNotFound, UserNotFound, TokenTypeIncorrect, TokenIsBlacklisted
class RefreshService:
    
    def __init__(self,
                 db_blacklisted_service : IBlacklistRepository,
                 db_user_service : IUserRepository,
                 db_token_service: IAuthTokensRepository,
                 jwt_service: IJWTService,
                 hash_token_service : IHashTokenService,
                 log_service : ILogRepo,
                 brute_service : IBruteService):
        
        self.db_blacklisted_service = db_blacklisted_service
        self.db_user_service = db_user_service
        self.db_token_service = db_token_service
        self.jwt_service = jwt_service
        self.hash_token_service = hash_token_service
        self.log_service = log_service
        self.brute_service = brute_service
        
    async def refresh(self, refresh_dto: RefreshDTO):
        
        refresh_token = refresh_dto.refresh_token
        
        if not refresh_token:
            await self.log_service.create_log(event_type="Refresh", username=None, user_id=None, status="Failed", ip=refresh_dto.ip, reason="Невозможно обновить токен, refresh токена нет!")
            raise ValueError("Refresh token обязателен!")
        
        
        blacklisted = self.db_blacklisted_service.find_blacklisted_by_token(token=self.hash_token_service.hash(refresh_token))
        if blacklisted:
            await self.log_service.create_log(event_type="Refresh", username=None, user_id=None, status="Failed", ip=refresh_dto.ip, reason="Невозможно обновить токен, он в черном списке!")
            raise TokenIsBlacklisted()
            
        try:
             payload = self.jwt_service.decode_jwt_token(refresh_token)
        except:
            await self.log_service.create_log(
                event_type="Refresh",username=None,  
                user_id=None, 
                status="Failed", 
                ip=refresh_dto.ip, 
                reason="Невозможно обновить токен, неверный тип токена!")
            
            raise TokenNotFound()
        
        if payload.get("type") != 'refresh':
            await self.log_service.create_log(event_type="Refresh",username=None,  user_id=None, status="Failed", ip=refresh_dto.ip, reason="Невозможно обновить токен, неверный тип токена!")
            raise TokenTypeIncorrect()
        
        user_id = payload.get("user_id")
        user_from_db = await self.db_user_service.get_user_by_user_id(user_id=user_id)
        
        if not user_from_db:
            await self.log_service.create_log(event_type="Refresh", username=None,user_id=None, status="Failed", ip=refresh_dto.ip, reason="Невозможно обновить токен, пользователь не найден!")
            raise UserNotFound()
        
        deleted = self.db_token_service.delete_refresh_token(user_id = user_from_db.id, hashed_token=self.hash_token_service.hash(refresh_token))
        if deleted == 0:
            await self.log_service.create_log(event_type="Refresh",username=user_from_db.username,  user_id=user_from_db.id, status="Failed", ip=refresh_dto.ip, reason="Невозможно обновить токен, токен не найден!")
            raise TokenNotFound()
            
        
        tokens = self.jwt_service.create_jwt_token(user_id = user_from_db.id, username=user_from_db.username)
        hashed_new_refresh = self.hash_token_service.hash(tokens['refresh'])
        
        new_refresh = AuthTokensDomainModel(
            id=None,
            user_id=user_from_db.id,
            refresh_token=hashed_new_refresh,
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            created_at=datetime.now(timezone.utc)
        )
        
        await self.db_token_service.create_token(new_refresh)
        
        hashed_blacklisted = self.hash_token_service.hash(refresh_token)
        
        new_blacklisted = BlacklistDomainModel(
            id=None,
            token=hashed_blacklisted,
            token_type='refresh',
            user_id=user_from_db.id, 
            reason='Токен обновлен',
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(days=30)
        )
        
        await self.db_blacklisted_service.create_blacklisted(new_blacklisted)

        await self.log_service.create_log(event_type="Refresh", username=user_from_db.username, user_id=user_from_db.id, status="Success", ip=refresh_dto.ip, reason="Токен успешно обновлен!")
        return RefreshDTO(refresh_token=tokens['refresh'], access_token=tokens['access'], ip=refresh_dto.ip)
    
    