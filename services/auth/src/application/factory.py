from fastapi import FastAPI
from src.application.lifespan import lifespan
from src.api import v1


def include_routers(app: FastAPI) -> None:
    app.include_router(v1.router)


def create_app() -> FastAPI:

    app = FastAPI(title="Auth Service", version="0.1.1", lifespan=lifespan)

    include_routers(app)

    return app
