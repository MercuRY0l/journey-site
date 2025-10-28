from fastapi import FastAPI
from database.models import UserModel
from sqlalchemy.orm import session
from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import HTTPBearer
from database.models import SessionLocal

app = FastAPI()



class SecurityConfig:
    security = HTTPBearer()

    SECRET_KEY = "qxlqxkqxmqxo1xo3xm23xox991xn3oxub3bcvuioqxmnqjklzbuxnbucvynniqxbug72xf64tvx4f65x6fg!G^f4x6f34g7uhxvyxx"
    ALGORITHM = ["HS256"]
    ACCSESS_TOKEN_EXPIRED = 30
    REFRESH_TOKEN_EXPIRED = 7
    



    

@app.get('register/', response_model=UserModel)
async def create_user(username):
    pass



    
    
    