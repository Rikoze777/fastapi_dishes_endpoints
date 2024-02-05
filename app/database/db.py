from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Config
from redis import Redis

Base = declarative_base()
config = Config()
database_url = config.POSTGRES_URL
engine = create_engine(database_url)
redis_host = config.REDIS_HOST
redis_port = config.REDIS_PORT

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_redis():
    cache = Redis(host=redis_host, port=redis_port, db=0)
    return cache


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
