from pydantic import BaseModel, field_validator

from typing import Optional


class ChangeUsername(BaseModel):
    new_username: str
    ip: Optional[str] = None
    
    @field_validator("new_username")
    def username_validator(cls, v):
        if len(v) < 5:
            raise ValueError("Имя пользователя должно быть минимум 5 символов")
        if len(v) > 50:
            raise ValueError("Имя пользователя не должно превышать 50 символов")
        return v
            
    
    
class ChangeEmail(BaseModel):
    new_email: str
    ip: Optional[str] = None
    
    @field_validator("new_email")
    def email_validator(cls,v ):
        if len(v) > 255:
            raise ValueError("Email не должен превышать 255 символов!")
    
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
    ip: Optional[str] = None

    @field_validator("old_password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов")
        if len(v) > 255:
            raise ValueError("Пароль должен быть менее 255 символов")

        return v
    
    
    @field_validator("new_password")
    def password_validator2(cls, v):
        if len(v) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов")
        if len(v) > 255:
            raise ValueError("Пароль должен быть менее 255 символов")

        return v
    
    