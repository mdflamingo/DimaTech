from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import settings
from db.postgres.models import Base

metadata = Base.metadata
dsn = (
    f"postgresql+asyncpg://"
    f"{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.db_host}:{settings.db_port}/{settings.postgres_db}"
)
engine = create_async_engine(dsn, echo=True, future=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
