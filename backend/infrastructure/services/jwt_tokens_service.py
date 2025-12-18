import jwt

import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from domain.interfaces.jwt_interface import IJWTService


load_dotenv()

SECRET_KEY = os.getenv(key="SECRET_KEY")

class JwtTokensService(IJWTService):        

    def create_jwt_token(self, user_id, username):
        access_token_payload = {
            'user_id': user_id,
            'username': username,
            'type' : 'access',
            'exp': datetime.now(timezone.utc) + timedelta(minutes=60),
            'iat': datetime.now(timezone.utc),
            
        }
        
        refresh_token_payload = {
            'user_id': user_id,
            'type' : 'refresh',
            'exp': datetime.now(timezone.utc) + timedelta(days=7),
            'iat': datetime.now(timezone.utc),
        }
        
        access_token = jwt.encode(
            access_token_payload, 
            SECRET_KEY, 
            algorithm='HS256'
        )
        
        refresh_token = jwt.encode(
            refresh_token_payload, 
            SECRET_KEY, 
            algorithm='HS256'
        )
        
        return {
            'access': access_token,
            'refresh': refresh_token,
        }
    
    def decode_jwt_token(self, token: str):
        try:
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Токен истёк")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Недействительный токен")