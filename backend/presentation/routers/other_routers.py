
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, Depends, Cookie
from fastapi.exceptions import HTTPException

from infrastructure.services.jwt_tokens_service import JwtTokensService
from infrastructure.repositories.user_repo import UserRepository


from infrastructure.repositories.user_repo import UserRepository

router = APIRouter()
templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@router.get("/fishing")
async def root(request: Request):
    return templates.TemplateResponse("fishing_page.html", {"request" : request})

@router.get("/hunting")
async def root(request: Request):
    return templates.TemplateResponse("hunting_page.html", {"request" : request})

@router.get("/about")
async def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request" : request})

@router.get("/contacts")
async def root(request: Request):
    return templates.TemplateResponse("contacts_page.html", {"request" : request})




async def get_current_user(
    access_token: str = Cookie(None),
):#TODO вынести в отдельный файл
    if not access_token:
        raise HTTPException(status_code=401)

    jwt_service = JwtTokensService()
    payload =  jwt_service.decode_jwt_token(access_token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401)

    repo = UserRepository()
    user = await repo.get_user_by_user_id(user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=401)

    
    return user


@router.get("/auth/me")
async def root(request: Request, user = Depends(get_current_user)):
    token = request.cookies.get("access_token") or request.cookies.get("access")
    
    if not token:
        raise HTTPException(status_code=401)
    
    
    if not user:
        raise HTTPException(status_code=401)
    
    return ({
        
        "username" : user.username,
        "email" : user.email
        
    })        
    