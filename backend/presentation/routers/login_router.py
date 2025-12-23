import traceback

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi import status

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.dto.login_dto import LoginDTO
from app.dto.login_service_dto import LoginServiceDTO

from app.services.login_service import LoginService

from domain.services.user_service import UserModelService
from domain.services.auth_tokens_service import AuthTokensModelService


from infrastructure.services.hash_pass_service import HashPassService
from infrastructure.services.hash_token_service import HashTokenService
from infrastructure.services.jwt_tokens_service import JwtTokensService
from infrastructure.services.brute_protection_service import BruteService

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.auth_tokens_repo import AuthTokensRepository
from infrastructure.repositories.log_repo import LogRepo

from domain.services.log_service import LogService

loginRouter = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


def get_login_service():
    
    
    user_repo = UserRepository()
    auth_repo = AuthTokensRepository()
    log_repo = LogRepo()
    
    return LoginService(
        db_user_service=UserModelService(repository=user_repo),
        db_token_service=AuthTokensModelService(repo=auth_repo),
        log_service=LogService(repo=log_repo),
        
        brute_service=BruteService(),
        hash_pass_service=HashPassService(), 
        hash_token_service=HashTokenService(),
        jwt_service=JwtTokensService(),
        
    )

@loginRouter.get('/auth/login')
async def login_get(request:Request):
    return templates.TemplateResponse("login.html", {'request' : request})

@loginRouter.post('/auth/login')
async def login_for_accsess_token(request : Request, data : LoginDTO, service = Depends(get_login_service)):

    client_host = request.client.host
    
    login_dto = LoginServiceDTO(
        username=data.username,
        password=data.password,
        ip=client_host
    )

    try:
        tokens = await service.login(login_dto=login_dto)
        
        response = JSONResponse({
            "success": True,
            "username" : login_dto.username
        })
        
        response.set_cookie(
            key = 'refresh_token', 
            path="/",
            value = tokens.refresh_token,
            httponly=True,
            secure=True,
            samesite="lax"
        )
        
        response.set_cookie(
            key='access_token',
            path='/',
            value=tokens.access_token,
            httponly=True,
            secure=True,
            samesite='lax'
        )
        
        return response
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при регистрации: {e}")