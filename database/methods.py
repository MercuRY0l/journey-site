from argon2 import PasswordHasher
from .models import SessionLocal, UserModel
from datetime import datetime

def create_users(username: str, email: str, password: str, created_at : datetime = None):
    db = SessionLocal()
    try:
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        
        if created_at == None:
            created_at = datetime.now() 
        
        user = UserModel(username=username, email=email, password=hashed_password, created_at=created_at)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        
create_users("example", "example@mail.ru", "example")