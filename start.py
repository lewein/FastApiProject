import uvicorn

from app.core.settings import settings

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host="127.0.0.1",
        port=settings.API_APP_PORT,
        lifespan='on', access_log=False, loop='uvloop', reload=True
    )
