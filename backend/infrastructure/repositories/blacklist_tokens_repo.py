from domain.interfaces.blacklist_interface import IBlacklistRepository
from domain.models.blacklist_domain_model import BlacklistDomainModel

from infrastructure.database.db_connector import SessionLocal
from infrastructure.database.models.blacklist_model import BlackListTokensModel

from sqlalchemy import delete
from sqlalchemy.future import select


def orm_to_domain(orm: BlackListTokensModel) -> BlacklistDomainModel:
    return BlacklistDomainModel(
        id=orm.id,
        token=orm.token,
        token_type=orm.token_type,
        user_id=orm.user_id,
        reason=orm.reason,
        created_at=orm.created_at,
        expires_at=orm.expires_at
    )

class BlackListTokenRepository(IBlacklistRepository):

    async def create_blacklisted(
        self,
        blacklisted: BlacklistDomainModel
    ) -> BlacklistDomainModel:

        async with SessionLocal() as session:
            
            orm = BlackListTokensModel(
            token=blacklisted.token,
            token_type=blacklisted.token_type,
            user_id=blacklisted.user_id,
            reason=blacklisted.reason,
            created_at=blacklisted.created_at,
            expires_at=blacklisted.expires_at
)
            
            session.add(orm)
            await session.commit()
            await session.refresh(orm)
            return orm_to_domain(orm)

    async def delete_blacklisted_by_token(self, token: str) -> None:
        async with SessionLocal() as session:
            stmt = delete(BlackListTokensModel).where(
                BlackListTokensModel.token == token
            )
            await session.execute(stmt)
            await session.commit()

    async def find_blacklisted_by_token(
        self,
        token: str
    ) -> BlacklistDomainModel | None:

        async with SessionLocal() as session:
            stmt = select(BlackListTokensModel).where(
                BlackListTokensModel.token == token
            )

            res = await session.execute(stmt)
            orm_token = res.scalars().first()
            
            return orm_to_domain(orm_token) if orm_token else None
