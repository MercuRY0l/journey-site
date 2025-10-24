
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy import create_engine
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class User(Base):
    __table_name__ = 'django_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_deault=func.now())


engine = create_engine("mssql+pyodbc://sa:kKXQJXJLxmxq!qxj133!xqxXcvb@THUNDEROBOT\\SQLEXPRESS/django_users?driver=ODBC+Driver+17+for+SQL+Server")
Base.metadata.create_all(engine)