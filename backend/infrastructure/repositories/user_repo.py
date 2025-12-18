from domain.interfaces.user_interface import IUserRepository
from domain.models.user_domain_model import UserDomainModel

from sqlalchemy import delete
from sqlalchemy.future import select

from infrastructure.database.db_connector import SessionLocal
from infrastructure.database.models.user_model import UserModel



def orm_to_domain(orm_user: UserModel) -> UserDomainModel:
    return UserDomainModel(
        id=orm_user.id,
        username=orm_user.username,
        password=orm_user.password,
        email=orm_user.email,
        created_at=orm_user.created_at
    )

class UserRepository(IUserRepository):

    async def create_user(self, user: UserDomainModel) -> UserDomainModel:
        async with SessionLocal() as session:
            orm_user = UserModel(
                username=user.username,
                email=user.email,
                password=user.password
            ) 
            session.add(orm_user)
            await session.commit()
            await session.refresh(orm_user)
            
            return orm_to_domain(orm_user)

    async def get_user_by_username(self, username: str) -> UserDomainModel | None:
        async with SessionLocal() as session:
            stmt = select(UserModel).where(UserModel.username == username)
            
            res = await session.execute(stmt)
            orm_user = res.scalars().first()
            
            return orm_to_domain(orm_user) if orm_user else None

    async def get_user_by_email(self, email: str) -> UserDomainModel | None:
        async with SessionLocal() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            
            res = await session.execute(stmt)
            orm_user = res.scalars().first()
            
            return orm_to_domain(orm_user) if orm_user else None

    async def get_user_by_user_id(self, user_id: int) -> UserDomainModel | None:
        async with SessionLocal() as session:
            stmt = select(UserModel).where(UserModel.id == user_id)
            
            res = await session.execute(stmt)
            orm_user = res.scalars().first()
            
            return orm_to_domain(orm_user) if orm_user else None

    async def delete_user(self, username: str) -> int:
        async with SessionLocal() as session:
            result = await session.execute(
                delete(UserModel).where(UserModel.username == username)
            )
            await session.commit()
            return result.rowcount
