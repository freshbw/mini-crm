from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api_router import api_router
from app.config import get_settings
from app.db.engine import create_engine, create_session_factory
from app.kv.client import create_valkey
from app.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    app.state.settings = settings
    setup_logging(json_logs=not settings.debug)

    engine = create_engine(settings)
    valkey = None

    try:
        app.state.engine = engine
        app.state.session_factory = create_session_factory(engine)
        valkey = await create_valkey(settings)
        app.state.valkey = valkey
        yield
    finally:
        try:
            if valkey is not None:
                await valkey.close()
        finally:
            await engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Mini-CRM API",
        version="0.0.1",
        description="Mini-CRM",
        lifespan=lifespan,
        docs_url="/api/docs" if settings.debug else None,
        openapi_url="/api/openapi.json" if settings.debug else None,
        redoc_url="/api/redoc" if settings.debug else None,
    )

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
