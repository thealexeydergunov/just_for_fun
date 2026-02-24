from asyncio import Semaphore
from collections.abc import Callable
from functools import lru_cache

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.settings import get_settings


@lru_cache
def get_semaphore() -> Semaphore:
    settings = get_settings()
    return Semaphore(value=settings.REQUEST_SEMAPHORE)


def setup_middlewares(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def semaphores(request: Request, call_next: Callable) -> Response:
        sem = get_semaphore()
        async with sem:
            response = await call_next(request)
        return response

    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

    return app
