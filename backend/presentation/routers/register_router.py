import traceback

from fastapi import Request, APIRouter, Depends
from fastapi import HTTPException, status, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.dto.register_dto import RegisterDTO
from app.dto.register_service_dto import RegisterServiceDTO

from app.services.register_service import RegisterService


from domain.services.user_service import UserModelService
from domain.services.auth_tokens_service import AuthTokensModelService

from infrastructure.services.hash_pass_service import HashPassService
from infrastructure.services.hash_token_service import HashTokenService
from infrastructure.services.jwt_tokens_service import JwtTokensService
from infrastructure.services.brute_protection_service import BruteService

from infrastructure.repositories.user_repo import UserRepository
from infrastructure.repositories.auth_tokens_repo import AuthTokensRepository
from infrastructure.repositories.log_repo import LogRepo

from pydantic import BaseModel, EmailStr

from domain.services.log_service import LogService

regRouter = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")
 
 
def get_reg_service():
    
    user_repo = UserRepository()
    auth_repo = AuthTokensRepository()
    log_repo = LogRepo()
    
    return RegisterService(
        db_user_service=UserModelService(repository=user_repo),
        db_token_service=AuthTokensModelService(repo=auth_repo),
        log_service = LogService(repo=log_repo),
        
        brute_service=BruteService(),
        hash_pass_service=HashPassService(),
        hash_token_service = HashTokenService(),
        jwt_service=JwtTokensService()
        
    )

@regRouter.get('/auth/register')
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {'request' : request})


@regRouter.post('/auth/register')
async def create_user(request : Request, 
                      data : RegisterDTO,
                      service = Depends(get_reg_service)):
    
    if data.password != data.password_repeat:
        return {"error" : "Пароли не совпадают!"}
    
    client_host = request.client.host
    
    reg_dto = RegisterServiceDTO(
        username=data.username,
        password=data.password,
        email=data.email,
        ip=client_host
    )
    
    try:
        tokens = await service.register(reg_dto=reg_dto)
    
        response = JSONResponse({
            "success": True,
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token
        })
        
        response.set_cookie(
            key="refresh_token",
            value = tokens.refresh_token,
            secure=True,
            httponly=True,
            samesite="lax"
            
        )
        
        return response
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка при регистрации: {e}")