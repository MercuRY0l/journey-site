
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship
from sqlalchemy import Column,String,Integer,DateTime, ForeignKey
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
        

class AuthTokensModel(Base):
    __tablename__ = "AuthTokens"
    
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("Users.ID", ondelete = "CASCADE"), nullable=False)
    refresh_token = Column(String(512), nullable=False, unique = True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("UserModel", backref="auth_tokens")
    
    
    def __repr__(self):
        return f"<AuthToken(user_id={self.user_id}, expires_at={self.expires_at})>"
     
class BlackListTokensModel(Base):
    __tablename__ = "BlackListTokens"
    
    id = Column("ID",Integer, primary_key=True, autoincrement=True)
    token = Column(String(512), nullable=False)
    token_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.ID", ondelete="SET NULL"))
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("UserModel", backref="blacklist_tokens")
    
    def __repr__(self):
        return f"<BlacklistedToken(user_id={self.user_id}, type={self.token_type}>"
    
engine = create_engine("mssql+pyodbc://sa:mnxjqqjxlJQXI!Cx@THUNDEROBOT\\SQLEXPRESS/fastapi_users?driver=ODBC+Driver+17+for+SQL+Server")
SessionLocal = sessionmaker(bind = engine)


