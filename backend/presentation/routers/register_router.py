
from fastapi import Request, APIRouter, Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from infrastructure.models.user_model import UserModel

from sqlalchemy.orm import Session

from infrastructure.config.connector import SessionLocal

from pydantic import BaseModel

from datetime import timedelta

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    email : str
    password : str
    password_repeat : str

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