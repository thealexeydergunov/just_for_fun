from typing import Annotated

from fastapi import APIRouter, Depends, Header
from starlette import status

from app.auth import get_api_key
from app.models.organisations import (
    OrganisationDetailResponseModel,
    OrganisationFilterModel,
    OrganisationListResponseModel,
)
from app.pg import AsyncSession, get_session
from app.service.organisations import get_organisations_service

router = APIRouter(prefix="/organisations", tags=["organisations"], dependencies=[Depends(get_api_key)])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[OrganisationListResponseModel],
    description="Get organisation list",
)
async def organisations_list(
    data_filter: Annotated[OrganisationFilterModel, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    _: str = Header(alias="X-AUTH-KEY"),
) -> list[OrganisationListResponseModel]:
    service = get_organisations_service()
    response = await service.get_list(session=session, data_filter=data_filter)
    return response


@router.get(
    "/{organisation_id}/",
    status_code=status.HTTP_200_OK,
    response_model=OrganisationDetailResponseModel,
    description="Get organisation detail",
)
async def organisations_detail(
    organisation_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
    _: str = Header(alias="X-AUTH-KEY"),
) -> OrganisationDetailResponseModel:
    service = get_organisations_service()
    response = await service.get_detail(session=session, organisation_id=organisation_id)
    return response
