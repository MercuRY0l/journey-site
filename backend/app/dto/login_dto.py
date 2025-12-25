

from pydantic import BaseModel, field_validator

class LoginDTO(BaseModel):
    
    username: str
    password: str
    
    
    @field_validator("username")
    def username_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Имя пользователя должно быть минимум 5 символов")
        if len(v) > 50:
            raise ValueError("Имя пользователя не должно превышать 50 символов")
        return v
            
    @field_validator("password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов")
        if len(v) > 255:
            raise ValueError("Пароль должен быть менее 255 символов")

        return v