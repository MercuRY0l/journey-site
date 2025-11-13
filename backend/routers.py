from fastapi import HTTPException, APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.models import UserModel, SessionLocal
from pydantic import BaseModel
from argon2 import PasswordHasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from tokens import Token

from starlette.status import HTTP_302_FOUND

from datetime import timedelta
from tokens import SecurityConfig, create_access_token, create_refresh_token, verify_token

router = APIRouter()

templates = Jinja2Templates(directory="C:/Users/udgit/Documents/site_project_fastapi/frontend/static/html")


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
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
async def create_user(request : Request, username: str = Form(...), email:str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    try:
        if UserModel.user_in_database(db, username):
            raise HTTPException(status_code=400, detail="Пользователь уже существует!")
            
            
        user = UserModel.create_user(
            db,
            username = username,
            password = hash_pass(password),
            email = email,

        )
        
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
        
        response = RedirectResponse(url = "/", status_code=HTTP_302_FOUND)
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
async def login_for_accsess_token(username:str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    try:
        
        
        user = UserModel.authenticate_user(db, username, password)
        print(user)
        
        if not user:
            raise HTTPException(status_code=401, detail="Пользователя не существует!")
        
        token_data = {
            "username" : username,
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