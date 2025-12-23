from datetime import datetime,timedelta,timezone

from domain.interfaces.user_interface import IUserRepository
from domain.interfaces.blacklist_interface import IBlacklistRepository
from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.interfaces.jwt_interface import IJWTService
from domain.interfaces.hash_tokens_service import IHashTokenService
from domain.interfaces.log_interface import ILogRepo
from domain.interfaces.brute_interface import IBruteService

from domain.models.blacklist_domain_model import BlacklistDomainModel
from domain.models.log_domain_model import LogDomainModel

from app.dto.logout_dto import LogoutDTO
from app.exceptions.logout_exceptions import TokenNotFound
class LogoutService:
    
    def __init__(self,
                db_user_service : IUserRepository,
                db_blacklisted_service : IBlacklistRepository,
                db_token_service : IAuthTokensRepository,
                jwt_service : IJWTService,
                hash_token_service : IHashTokenService,
                log_service : ILogRepo,
                brute_service : IBruteService):
        
        self.db_user_service = db_user_service
        self.db_blacklisted_service = db_blacklisted_service
        self.db_token_service = db_token_service
        self.jwt_service = jwt_service
        self.hash_token_service = hash_token_service
        self.log_service = log_service
        self.brute_service = brute_service
    
    async def logout(self, logout_dto : LogoutDTO):
    
        refresh_token = logout_dto.refresh_token
        
        
        if not refresh_token: 
            await self.log_service.create_log(LogDomainModel(event_type="Logout", username=None, user_id=None, status="Failed", ip=logout_dto.ip, reason="Выход невозможен, refresh токен не найден!"))
            raise TokenNotFound()
            
        payload = self.jwt_service.decode_jwt_token(refresh_token)
        user_id = payload.get("user_id") if payload else None
        user_in_db = await self.db_user_service.get_user_by_user_id(user_id=user_id)
        
        hashed_token = self.hash_token_service.hash(refresh_token)
        
        
        deleted = await self.db_token_service.delete_refresh_token(user_id=user_id, hashed_token=hashed_token)
        if not deleted:
            await self.log_service.create_log(LogDomainModel(event_type="Logout", username=user_in_db.username , user_id=user_in_db.id, status="Failed", ip=logout_dto.ip, reason="Выход невозможен, refresh токен не найден!"))
            raise TokenNotFound() 
                    
        blacklisted_token = self.hash_token_service.hash(token=refresh_token)
        
        
        blacklisted = BlacklistDomainModel(
            id=None,
            token=blacklisted_token,
            token_type="refresh",
            user_id=user_id,
            reason="Выход пользователя из аккаунта",
            expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            created_at=datetime.now(timezone.utc)
        )
        
        await self.db_blacklisted_service.create_blacklisted(blacklisted)
        
        await self.log_service.create_log(LogDomainModel(event_type="Logout", username = user_in_db.username, user_id=user_in_db.id, status="Success", ip=logout_dto.ip, reason="Успешный выход!"))
        return {"status" : "succses"}
                
        
            