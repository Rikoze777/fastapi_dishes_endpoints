import logging
from typing import Annotated, AsyncGenerator, AsyncIterator
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy_utils import database_exists, create_database
from app.config import Config

logger = logging.getLogger(__name__)

config = Config()

# engine = create_async_engine(config.ENGINE_URL, echo=False)

# if not database_exists(config.POSTGRES_URL):
#     create_database(config.POSTGRES_URL)

# async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         yield session

async_engine = create_async_engine(
    config.ENGINE_URL,
    pool_pre_ping=True,
    echo=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    expire_on_commit=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

# import contextlib
# from typing import AsyncIterator

# from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
#                                     async_sessionmaker, create_async_engine)
# from sqlalchemy.orm import declarative_base


# Base = declarative_base()


# class DatabaseSessionManager:
#     def __init__(self):
#         self._engine: AsyncEngine | None = None
#         self._sessionmaker: async_sessionmaker | None = None

#     def init(self, host: str):
#         self._engine = create_async_engine(host)
#         self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

#     async def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         await self._engine.dispose()
#         self._engine = None
#         self._sessionmaker = None

#     @contextlib.asynccontextmanager
#     async def connect(self) -> AsyncIterator[AsyncConnection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 await connection.rollback()
#                 raise

#     @contextlib.asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         session = self._sessionmaker()
#         try:
#             yield session
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()

#     # Used for testing
#     async def create_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.create_all)

#     async def drop_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.drop_all)


# sessionmanager = DatabaseSessionManager()


# async def get_db():
#     async with sessionmanager.session() as session:
#         yield session


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config import Config


# config = Config()
# database_url = config.POSTGRES_URL
# engine = create_engine(database_url)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
