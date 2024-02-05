from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB_TEST: str = 'dishes_test'
    POSTGRES_URL: str
    TESTBASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    class Config:
        env_file = './.env'
