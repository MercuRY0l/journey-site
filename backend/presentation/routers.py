from fastapi import HTTPException, APIRouter, Depends, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.models.user_model import UserModel
from database.models.auth_tokens_model import AuthTokensModel
from database.models.blacklisted_tokens_model import BlackListTokensModel

from backend.database.config.connector import SessionLocal

from pydantic import BaseModel
from argon2 import PasswordHasher
from fastapi.security import OAuth2PasswordBearer

from starlette.status import HTTP_302_FOUND

from datetime import timedelta

from tokens import SecurityConfig, create_access_token, create_refresh_token, verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")

class UserCreate(BaseModel):
    username : str
    email: str
    password: str
    password_repeat:str
    
class UserLogin(BaseModel):
    username: str
    password: str
    
   
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def hash_pass(password: str) -> str:
    ph = PasswordHasher()
    hashed_password = ph.hash(password)
    return hashed_password


@router.get("/")
def root(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})

@router.get("/fishing")
def root(request: Request):
    return templates.TemplateResponse("fishing_page.html", {"request" : request})

@router.get("/hunting")
def root(request: Request):
    return templates.TemplateResponse("hunting_page.html", {"request" : request})

@router.get("/about")
def root(request: Request):
    return templates.TemplateResponse("about_us.html", {"request" : request})

@router.get('/auth/register')
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {'request' : request})

@router.get('/auth/login')
async def login_get(request:Request):
    return templates.TemplateResponse("login.html", {'request' : request})

@router.post('/auth/register')
async def create_user(request : Request, user: UserCreate, db: Session = Depends(get_db)):
    try:
        if UserModel.user_in_database(db, user.username):
            raise HTTPException(status_code=400, detail="Пользователь уже существует!")
        
        try:
            user_obj = UserModel.create_user(
                db,
                username = user.username,
                password = hash_pass(user.password),
                email = user.email,

            ) 
            
        except Exception as e:
            print("Ошибка создания пользователя:", e)
            raise HTTPException(status_code=400, detail=f"Ошибка БД: {e}")
        
        token_data = {
            "username" : user_obj.username,
            "user_id" : user_obj.id,
            "email" : user_obj.email
        }
        
        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE)
        access_token = create_access_token(
            data = token_data,
            expires_delta=access_token_expires
        )
        
        response = JSONResponse({"success": True, "username": user_obj.username})
        response.set_cookie(
            key = 'access_token',
            value=access_token,
            httponly=True,
            secure=False
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Не удалось подключитьсяк бд: {e}")
    

@router.post('/auth/login')
async def login_for_accsess_token(user: UserLogin, db: Session = Depends(get_db)):
    try:
        user = UserModel.get_user_by_name(user.username)
        
        if not user:
            raise HTTPException(status_code=401, detail="Пользователя не существует!")
        
        token_data = {
            "username" : user.username,
            "user_id" : user.id,
            "email" : user.email
        }
        
        access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE)
        access_token = create_access_token(
            data = token_data,
            expires_delta=access_token_expires
        )
        
        refresh_token = create_refresh_token(data = token_data)
        
        response = RedirectResponse(url='/', status_code=HTTP_302_FOUND)    
        response.set_cookie(
            key = 'access',
            value = access_token,
            httponly=True,
            secure=False
        )
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при аутентификации:{str(e)}"
        )
        
@router.post('/auth/logout')
async def logout(token : str = Depends(oauth2_scheme)):
    pass
    
    