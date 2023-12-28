from typing import AsyncGenerator
from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_scoped_session
from app.core.config import setting


class Database:
    def __init__(self):
        self.engine = create_async_engine(url=setting.DB_URL, echo=True)
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(session_factory=self.session, scopefunc=current_task)
        return session


db = Database()


async def get_db() -> AsyncGenerator[AsyncGenerator, None]:
    async with db.session() as session:
        yield session
