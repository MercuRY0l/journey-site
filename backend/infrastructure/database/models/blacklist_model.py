
from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from ..db_connector import Base

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
        return f"<BlacklistedToken(user_id={self.user_id}, type={self.token_type})>"
 