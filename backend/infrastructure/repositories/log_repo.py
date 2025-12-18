
from infrastructure.database.db_connector import SessionLocal
from infrastructure.database.models.log_model import Log

from domain.interfaces.log_interface import ILogRepo
from domain.models.log_domain_model import LogDomainModel

from sqlalchemy import delete
from sqlalchemy.future import select


def orm_to_domain(log : Log) -> LogDomainModel:
    return LogDomainModel(
        event_type=log.event_type,
        username = log.username,
        user_id= log.user_id,
        status= log.status,
        ip = log.ip,
        reason= log.reason
    )

class LogRepo(ILogRepo):
    async def create_log(self, log: LogDomainModel):
        async with SessionLocal() as session:
            
            orm_log = Log(
                event_type=log.event_type,
                username = log.username,
                user_id= log.user_id,
                status= log.status,
                ip = log.ip,
                reason= log.reason
            )
            
            session.add(orm_log)
            await session.commit()
            await session.refresh(orm_log)
            
            return orm_to_domain(orm_log)
            
    
    async def delete_log(self, user_id : int):
        async with SessionLocal() as session:
            stmt = delete(Log).where(Log.user_id == user_id)
            await session.execute(stmt)
            await session.commit()
    
    async def find_log(self, user_id):
        async with SessionLocal() as session:
            stmt = select(Log).where(Log.user_id == user_id)
            
            res = await session.execute(stmt)
            orm_log = res.scalars().first()
            
            return orm_to_domain(orm_log)