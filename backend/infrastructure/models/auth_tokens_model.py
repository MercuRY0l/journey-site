

from sqlalchemy import Column,String,Integer,DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..base import Base

class AuthTokensModel(Base):
    __tablename__ = "AuthTokens"
    
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer, ForeignKey("Users.id", ondelete = "CASCADE"), nullable=False)
    refresh_token = Column(String(512), nullable=False, unique = True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("UserModel", backref="auth_tokens")
    
    
    def __repr__(self):
        return f"<AuthToken(user_id={self.user_id}, expires_at={self.expires_at})>"