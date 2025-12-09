

from sqlalchemy import Column,String,Integer,DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..base import Base

class BlackListTokensModel(Base):
    __tablename__ = "BlackListTokens"
    
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    token = Column(String(512), nullable=False)
    token_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="SET NULL"))
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("UserModel", backref="blacklist_tokens")
    
    def __repr__(self):
        return f"<BlacklistedToken(user_id={self.user_id}, type={self.token_type}>"