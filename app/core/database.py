import datetime
import databases

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from redis import Redis

from .settings import settings
from app.core.utils import logger


DATABASE_URL = settings.DATABASE_URL.format(settings.DB_USER, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_NAME)
CONNECT_ON_MSG = 'Database connect opened at {}'
CONNECT_OFF_MSG = 'Database connect closed at {}'

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
database = databases.Database(DATABASE_URL)


async def connect_db():
    try:
        await database.connect()
        logger.info(CONNECT_ON_MSG.format(datetime.datetime.now()))
    except Exception as ex:
        logger.error(f'Database connection ERROR - {ex}')


async def disconnect_db():
    try:
        await database.disconnect()
        logger.info(CONNECT_ON_MSG.format(datetime.datetime.now()))
    except Exception as ex:
        logger.error(f'Database disconnection ERROR - {ex}')


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as app_session:
        yield app_session


def get_redis() -> Redis:
    try:
        rd = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB
        )
        return rd
    except Exception as ex:
        logger.info(f'Redis launch exception - {ex}')


redis_db = get_redis()
