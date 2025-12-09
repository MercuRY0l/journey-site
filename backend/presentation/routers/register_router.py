
from fastapi import Request, APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from app.dto.register_dto import RegisterDTO
from app.services.register_service import RegisterService

from domain.services.user_service import UserModelService
from domain.services.auth_tokens_service import AuthTokensModelService
from domain.services.hash_service import HashService
from domain.services.jwt_tokens_service import JwtTokensService

regRouter = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")



 
def get_reg_service():
    return RegisterService(
        db_user_service=UserModelService(),
        db_tokens_service=AuthTokensModelService(),
        hash_service=HashService(),
        jwt_service=JwtTokensService()
    )

@regRouter.get('/auth/register')
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {'request' : request})


@regRouter.post('/auth/register')
async def create_user(request : Request, reg_dto: RegisterDTO, service = Depends(get_reg_service)):
    try:
        
        service.register(register_dto=reg_dto)
    
        response = JSONResponse({"success": True})
        response.set_cookie(
            key = 'access_token',
            value="access_token",
            httponly=True,
            secure=False
        )
        
        return response
    
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Не удалось подключитьсяк бд: {e}")
    
    except HTTPException as http_exception:
        raise http_exception
     