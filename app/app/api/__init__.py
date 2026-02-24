from fastapi import APIRouter

from ..settings import get_settings
from . import organisations, ping

settings = get_settings()

router = APIRouter(prefix=f"/api/{settings.API_VERSION}")
router.include_router(ping.router)
router.include_router(organisations.router)
