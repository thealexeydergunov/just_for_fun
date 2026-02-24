from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/", status_code=status.HTTP_200_OK)
async def ping() -> dict:
    return {"success": True}
