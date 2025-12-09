from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.dto.login_dto import LoginDTO
from app.services.login_service import LoginService

from domain.services.user_service import UserModelService
from domain.services.auth_tokens_service import AuthTokensModelService
from domain.services.blacklist_service import BlackListTokensModelService
from domain.services.hash_service import HashService
from domain.services.jwt_tokens_service import JwtTokensService

loginRouter = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


def get_login_service():
    return LoginService(
        db_user_service=UserModelService(),
        db_tokens_service=AuthTokensModelService(),
        db_blacklist_service=BlackListTokensModelService(),
        hash_service=HashService(),
        jwt_service=JwtTokensService()
    )

@loginRouter.get('/auth/login')
async def login_get(request:Request):
    return templates.TemplateResponse("login.html", {'request' : request})

@loginRouter.post('/auth/login')
async def login_for_accsess_token(request : Request, login_dto : LoginDTO, service = Depends(get_login_service)):

    try:
        service.login(login_dto=login_dto)
        
        response = JSONResponse({"status" : "auntificated!"})
        response.set_cookie(
            key = 'access',
            value = "", #TODO передать access в заголовок!
            httponly=True,
            secure=False
        )
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при аутентификации:{str(e)}"
        )