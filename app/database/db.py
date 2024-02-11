import logging
from collections.abc import AsyncIterator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import Config

logger = logging.getLogger(__name__)

config = Config()
redis_host = config.REDIS_HOST
redis_port = config.REDIS_PORT


class Base(DeclarativeBase):
    pass


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
