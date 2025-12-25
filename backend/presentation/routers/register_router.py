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

from domain.services.log_service import LogService

from pydantic import ValidationError

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
            "username" : reg_dto.username,
            "email" : reg_dto.email
        })
        
        response.set_cookie(
            key="refresh_token",
            path="/",
            value = tokens.refresh_token,
            secure=False,
            httponly=True,
            samesite="Lax"
            
        )
        
        response.set_cookie(
            key='access_token',
            path='/',
            value=tokens.access_token,
            httponly=True,
            secure=False,
            samesite='lax'
        )
        
        return response
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    except ValidationError as ve:
        errors = {}
        for err in ve.errors():
            field = err["loc"][0]
            errors[field] = err["msg"]

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    
    
    
    
    
    