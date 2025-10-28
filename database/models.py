
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



engine = create_engine("mssql+pyodbc://sa:mnxjqqjxlJQXI!Cx@THUNDEROBOT\\SQLEXPRESS/fastapi_users?driver=ODBC+Driver+17+for+SQL+Server")
SessionLocal = sessionmaker(bind = engine)


