from domain.interfaces.auth_tokens_interface import IAuthTokensRepository
from domain.models.auth_tokens_domain_model import AuthTokensDomainModel

from infrastructure.database.db_connector import SessionLocal
from infrastructure.database.models.auth_tokens_model import AuthTokensModel

from sqlalchemy import delete
from sqlalchemy.future import select

def orm_to_domain(orm: AuthTokensModel) -> AuthTokensDomainModel:
    return AuthTokensDomainModel(
        id=orm.id,
        user_id=orm.user_id,
        refresh_token=orm.refresh_token,
        expires_at=orm.expires_at,
        created_at=orm.created_at
    )

class AuthTokensRepository(IAuthTokensRepository):

    async def create_token(self, token: AuthTokensDomainModel) -> AuthTokensDomainModel:
        async with SessionLocal() as session:
            orm_token = AuthTokensModel(
                user_id=token.user_id,
                refresh_token=token.refresh_token,
                expires_at=token.expires_at
            )

            session.add(orm_token)
            await session.commit()
            await session.refresh(orm_token)

            return orm_to_domain(orm_token)

    async def delete_refresh_by_id(self, token_id: int) -> None:
        async with SessionLocal() as session:
            stmt = delete(AuthTokensModel).where(AuthTokensModel.id == token_id)
            await session.execute(stmt)
            await session.commit()

    async def delete_refresh_token(self, user_id: int, hashed_token: str) -> int:
        async with SessionLocal() as session:
            stmt = delete(AuthTokensModel).where(
                AuthTokensModel.user_id == user_id,
                AuthTokensModel.refresh_token == hashed_token
            )            
            res = await session.execute(stmt)
            await session.commit()
            return res.rowcount

    async def get_all_refresh_hashes(self, user_id: int) -> list[tuple[str, int]]:
        async with SessionLocal() as session:
            stmt = select(
                AuthTokensModel.refresh_token,
                AuthTokensModel.id
            ).where(AuthTokensModel.user_id == user_id)
            res = await session.execute(stmt)
            return res.scalars().all()

    async def find_token_by_userid(self, user_id: int) -> AuthTokensDomainModel | None:
        async with SessionLocal() as session:
            stmt = select(AuthTokensModel).where(
                AuthTokensModel.user_id == user_id
            )

            res = await session.execute(stmt)
            orm_token = res.scalars().first()
            
            return orm_to_domain(orm_token) if orm_token else None 

    async def find_token_by_refresh(self, refresh_token: str) -> AuthTokensDomainModel | None:
        async with SessionLocal() as session:
            stmt = select(AuthTokensModel).where(
                AuthTokensModel.refresh_token == refresh_token
            )

            res = await session.execute(stmt)
            orm_token = res.scalars().first()
            return orm_to_domain(orm_token) if orm_token else None
