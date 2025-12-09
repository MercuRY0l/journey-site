
from app.dto.register_dto import RegisterDTO

from domain.services.user_service import UserModelService
from domain.services.auth_tokens_service import AuthTokensModelService
from domain.services.hash_service import HashService
from domain.services.jwt_tokens_service import JwtTokensService

from datetime import datetime, timezone, timedelta
class RegisterService:
    
    def __init__(self,
                 db_user_service : UserModelService, 
                 db_tokens_service : AuthTokensModelService,
                 hash_service : HashService,
                 jwt_service : JwtTokensService):
        
        
        self.db_user_service = db_user_service
        self.db_tokens_service = db_tokens_service
        self.hash_service = hash_service
        self.jwt_service = jwt_service
    
    def register(self, register_dto : RegisterDTO):
        
        if self.db_user_service.user_in_database(register_dto.username):
            return{"error" : "User already exists!"}
        
        
        user = self.db_user_service.create_user(
            username = register_dto.username,
            password = self.hash_service.hash(register_dto.password),
            email = register_dto.email
        )
            
        
        tokens = self.jwt_service.create_tokens(user_id = user.id, username = user.username)
        access_token = tokens['access']
        refresh_token = tokens['refresh']
        
        self.db_tokens_service.create_token(user_id=user.id, refresh_token=refresh_token, expires_at=datetime.now(timezone.utc) + timedelta(days=30))
        
        return{"message" : "User successfully registered!"}