from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.core.utils import logger
from app.core.database import connect_db, disconnect_db
from app.core.settings import settings
from app.routes.routes import setup_routes


async def startup_app():
    try:
        await connect_db()
        logger.info('The application is start up')
    except Exception as ex:
        logger.error(f'The application couldn`t start up: {ex}')


async def shutdown_app():
    await disconnect_db()
    logger.error('The application is shutdown')


middleware = [
    Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
]


app = FastAPI(
    middleware=middleware,
    on_startup=[startup_app],
    on_shutdown=[shutdown_app]
)

setup_routes(app)


@app.get("/")
async def root():
    return {"message": "Sausage party"}




