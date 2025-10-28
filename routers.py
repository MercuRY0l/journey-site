from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from database.models import UserModel, SessionLocal
from pydantic import BaseModel
from argon2 import PasswordHasher
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from tokens import Token


router = APIRouter(prefix="/auth", tags=["authentification"])

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
        
def hash_pass(user_data : UserModel):
    ph = PasswordHasher()
    hashed_password = ph.hash(user_data.password)
    return hashed_password

@router.post('/register')
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        if UserModel.user_in_database(db, user_data.username):
            raise HTTPException(status_code=400, detail="Пользователь уже существует!")
        
        user = UserModel.create_user(
            db,
            username = user_data.username,
            password = hash_pass(user_data),
            email = user_data.email,

        )
        
        
        response_data =  {"message" : "Пользователь успешно зарегистрирован!", "user_id" : user.id}
        return response_data
          
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Не удалось подключитьсяк бд: {e}")
    
        
@router.post('/login')
async def login_for_accsess_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token: