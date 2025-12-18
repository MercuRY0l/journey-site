from sqlalchemy import Column, String, Integer, DateTime, func
from infrastructure.database.db_connector import Base

class UserModel(Base):
    __tablename__ = "Users"
    
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    username = Column("Username", String(50), unique=True, nullable=False)
    password = Column("Password", String(255), nullable=False)
    email = Column("Email", String(255), unique=True, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.sysdatetime())
    
    def __repr__(self):
        return f"<UserModel(id={self.username}, username={self.username})>"
