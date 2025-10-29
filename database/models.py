
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def create_user(cls, db, username: str, email: str, password: str):
        user = cls(username = username, email = email, password = password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @classmethod
    def get_user_by_name(cls, db, username:str):
        return db.query(cls).filter(cls.username == username).first()
        
    @classmethod
    def user_in_database(cls, db: Session, username: str) -> bool:
        user = cls.get_user_by_name(db, username)
        return user is not None
    
    @classmethod
    def authenticate_user(cls, db: Session, username : str, password : str):
        user = cls.get_user_by_name(db, username)
        if not user:
            return False
        
        ph = PasswordHasher()
        try:
            ph.verify(user.password, password)
            return user
        
        except VerifyMismatchError:
            return False
        
        except Exception as e:
            return False    
        
    
    
engine = create_engine("mssql+pyodbc://sa:mnxjqqjxlJQXI!Cx@THUNDEROBOT\\SQLEXPRESS/fastapi_users?driver=ODBC+Driver+17+for+SQL+Server")
SessionLocal = sessionmaker(bind = engine)


