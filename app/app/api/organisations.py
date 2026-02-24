from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.models.organisations import (
    OrganisationDetailResponseModel,
    OrganisationFilterModel,
    OrganisationListResponseModel,
)
from app.pg import AsyncSession, get_session
from app.service.organisations import get_organisations_service

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrganisationListResponseModel])
async def organisations_list(
    data_filter: Annotated[OrganisationFilterModel, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[OrganisationListResponseModel]:
    service = get_organisations_service()
    response = await service.get_list(session=session, data_filter=data_filter)
    return response


@router.get("/{organisation_id}/", status_code=status.HTTP_200_OK, response_model=OrganisationDetailResponseModel)
async def organisations_detail(
    organisation_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OrganisationDetailResponseModel:
    service = get_organisations_service()
    response = await service.get_detail(session=session, organisation_id=organisation_id)
    return response
