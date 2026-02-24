from functools import lru_cache

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.settings import get_settings


@lru_cache
def get_api_header() -> APIKeyHeader:
    return APIKeyHeader(name="X-AUTH-KEY", auto_error=True)


async def get_api_key(
    api_key: str = Security(get_api_header()),
) -> str:
    settings = get_settings()
    if api_key == settings.API_AUTH_KEY:
        return api_key

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )
