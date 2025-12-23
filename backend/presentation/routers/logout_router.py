
from fastapi.routing import APIRouter
from fastapi import Depends, Response
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from infrastructure.repositories.auth_tokens_repo import AuthTokensRepository
from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.blacklist_tokens_repo import BlackListTokenRepository
from infrastructure.repositories.log_repo import LogRepo

from app.dto.logout_dto import LogoutDTO
from app.services.logout_service import LogoutService

from domain.services.auth_tokens_service import AuthTokensModelService
from domain.services.user_service import UserModelService
from domain.services.blacklist_token_service import BlackListTokensModelService
from domain.services.log_service import LogService

from infrastructure.services.jwt_tokens_service import JwtTokensService
from infrastructure.services.hash_token_service import HashTokenService
from infrastructure.services.brute_protection_service import BruteService



logout_router = APIRouter()


def get_logout_service():
    
    auth_tokens_repo = AuthTokensRepository()
    user_repo = UserRepository()
    blacklist_repo = BlackListTokenRepository()
    log_repo = LogRepo()
    
    return LogoutService(
        db_user_service=UserModelService(user_repo),
        db_blacklisted_service=BlackListTokensModelService(blacklist_repo),
        db_token_service=AuthTokensModelService(auth_tokens_repo),
        jwt_service=JwtTokensService(),
        hash_token_service=HashTokenService(),
        log_service=LogService(log_repo),
        brute_service=BruteService()
        
        
    )


@logout_router.post("/auth/logout")
async def logout(response: Response, request: Request,  service=Depends(get_logout_service)):
    
    refesh_token = request.cookies.get("refresh_token") or request.cookies.get("refresh")
    ip = request.client.host
    
    dto = LogoutDTO(
        refresh_token=refesh_token,
        ip=ip
    )
    
    try:
        await service.logout(logout_dto=dto)
        
        response.delete_cookie(key="refresh_token", 
                               path="/",
                               httponly=True,
                               secure=True,
                               samesite="Lax") 
        
        
        response.delete_cookie(
            key='access_token',
            path='/',
            httponly=True,
            secure=True,
            samesite='lax'
        )
        
        
        response = JSONResponse({"status" : "success" , "message" : "Пользователь успешно вышел из аккаунта"})
        return response
        
    except Exception as e:
        print(e)
    
    




