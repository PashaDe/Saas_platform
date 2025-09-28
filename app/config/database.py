from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings


engine = create_async_engine(settings.database_url, future=True, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


