import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api import router
from app.handlers import setup_handlers
from app.lifespan import lifespan
from app.middlewares import setup_middlewares
from app.settings import get_settings

settings = get_settings()
app = FastAPI(
    title="API just for fun service docs",
    docs_url=f"/api/{settings.API_VERSION}/docs/",
    redoc_url=f"/api/{settings.API_VERSION}/redoc/",
    openapi_url=f"/api/{settings.API_VERSION}/openapi.json",
    servers=[
        {"url": "/"},
    ],
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
app.include_router(router)
setup_middlewares(app)
setup_handlers(app)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, log_level=settings.LOG_LEVEL)
