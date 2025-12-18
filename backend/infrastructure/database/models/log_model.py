

from sqlalchemy import Column, String, Integer, DateTime, func
from infrastructure.database.db_connector import Base

class Log(Base):
    
    __tablename__ = "UsersLog"
    __table_args__ = {"schema": "dbo"}
    
    id = Column("ID", Integer, primary_key=True, autoincrement=True)
    event_type = Column("event_type", String(255), nullable=False)
    username = Column("username", String(255))
    user_id = Column("user_id", Integer)
    status = Column("status", String(255), nullable=False)
    ip = Column("ip", String(255))
    reason = Column("reason", String(255), nullable=False)
    time = Column("time", DateTime(timezone=True), server_default=func.sysdatetime())
    
