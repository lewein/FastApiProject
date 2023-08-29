from fastapi import FastAPI

from app.routes import users, cities, common_requests


def setup_routes(app: FastAPI) -> None:
    app.include_router(users.router)
    app.include_router(cities.router)
    app.include_router(common_requests.router)
    return
