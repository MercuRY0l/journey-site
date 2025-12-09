
from ...app.dto.login_dto import LoginDTO

from ...domain.services.auth_tokens_service import AuthTokensModelService
from ...domain.services.user_service import UserModelService
from ...domain.services.blacklist_service import BlackListTokensModelService
from ...domain.services.hash_service import HashService
from ...domain.services.jwt_tokens_service import JwtTokensService

class LoginService:
    def __init__(self, db_user_service: UserModelService, 
                 db_tokens_service : AuthTokensModelService, 
                 db_blacklist_service : BlackListTokensModelService,
                 hash_service : HashService,
                 jwt_service : JwtTokensService):
        
        self.db_user_service = db_user_service
        self.db_tokens_service = db_tokens_service
        self.db_blacklist_service = db_blacklist_service
        self.hash_service = hash_service
        self.jwt_service = jwt_service
    
    def login(self, login_dto : LoginDTO):
    
    
        user = self.db_user_service.get_user_by_name(login_dto.username)
        
        if not user:
            return{"error" : "User is not exists"}
        
        tokens = self.jwt_service.create_jwt_token(user.id, user.username)
        
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        hashed_refresh = self.hash_service(refresh_token)
        
        self.db_tokens_service.create_token(user_id=user.id, refresh_token=hashed_refresh)
        
        return {"message" : "User is aunthificate!"}
        
