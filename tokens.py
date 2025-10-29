
import jwt

from fastapi.security import HTTPBearer
from datetime import timedelta, datetime, timezone
from typing import Optional
from pydantic import BaseModel

class SecurityConfig:
    security = HTTPBearer()

    SECRET_KEY = "qxlqxkqxmqxo1xo3xm23xox991xn3oxub3bcvuioqxmnqjklzbuxnbucvynniqxbug72xf64tvx4f65x6fg!G^f4x6f34g7uhxvyxx"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE = 30
    REFRESH_TOKEN_EXPIRE = 7

class Token(BaseModel):
    access_token : str
    token_type : str
    refresh_token : Optional[str] = None
    
    
def create_access_token(data: dict, expired_delta : timedelta | None = None):
    to_encode = data.copy()
    if expired_delta:
        expire = datetime.now(timezone.utc) + expired_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SecurityConfig.SECRET_KEY , SecurityConfig.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    expires_delta = timedelta(days=SecurityConfig.REFRESH_TOKEN_EXPIRE)
    return create_access_token(data, expires_delta)

def verify_token(token : str):
    try:
        payload = jwt.decode(token, SecurityConfig.SECRET_KEY, algorithms=[SecurityConfig.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
        


