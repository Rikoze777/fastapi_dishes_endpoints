from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config


config = Config()

DATABASE_URL = f"postgresql+psycopg2://{config.PROD_DB_USER}:{config.PROD_DB_PASSWORD}@{config.PROD_DB_HOST}:{config.PROD_DB_PORT}/{config.PROD_DB_NAME}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
