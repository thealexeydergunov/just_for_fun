from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.models.organisations import OrganisationDetailResponse, OrganisationFilter, OrganisationListResponse
from app.pg import AsyncSession, get_session
from app.service.organisations import get_organisations_service

router = APIRouter(prefix="/organisations", tags=["organisations"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrganisationListResponse])
async def organisations_list(
    data_filter: Annotated[OrganisationFilter, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[OrganisationListResponse]:
    service = get_organisations_service()
    response = await service.get_list(session=session, data_filter=data_filter)
    return response


@router.get("/{organisation_id}/", status_code=status.HTTP_200_OK, response_model=OrganisationDetailResponse)
async def organisations_detail(
    organisation_id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> OrganisationDetailResponse:
    service = get_organisations_service()
    response = await service.get_detail(session=session, organisation_id=organisation_id)
    return response
