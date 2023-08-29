from pydantic import BaseSettings
from .utils import load_env


class Settings(BaseSettings):
    APP_NAME: str = 'calculate_route'
    ADMIN: str = 'lean'
    AUTHOR: str = 'lewein'
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    APP_PORT: int
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = '.env.config'
        env_file_encoding = 'utf-8'


load_env()
settings = Settings()
