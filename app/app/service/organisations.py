from functools import lru_cache

from sqlalchemy.orm import selectinload
from sqlmodel import func, select, union_all

from app.exceptions import OrganisationNotFoundError
from app.models.activities import ActivityModel
from app.models.organisations import (
    ActivityResponse,
    OrganisationActivityModel,
    OrganisationDetailResponse,
    OrganisationFilter,
    OrganisationListResponse,
    OrganisationModel,
    PhoneResponse,
)
from app.pg import AsyncSession


class OrganisationsService:
    @staticmethod
    def _filter_by_activity_id(statement, activity_id: int):  # noqa: ANN205, ANN001
        sel_children_1 = select(ActivityModel.id).where(ActivityModel.parent_id == activity_id)
        sel_children_2 = select(ActivityModel.id).where(ActivityModel.parent_id.in_(sel_children_1))
        sel_parent = select(ActivityModel.id).where(ActivityModel.id == activity_id)
        all_activity_ids = union_all(sel_parent, sel_children_1, sel_children_2).subquery()
        sel_org_ids = (
            select(OrganisationActivityModel.organisation_id).where(
                OrganisationActivityModel.activity_id.in_(all_activity_ids)
            )
        ).subquery()
        return statement.where(OrganisationModel.id.in_(sel_org_ids))

    async def get_list(self, session: AsyncSession, data_filter: OrganisationFilter) -> list[OrganisationListResponse]:
        statement = select(OrganisationModel)
        if data_filter.activity_id:
            statement = self._filter_by_activity_id(statement=statement, activity_id=data_filter.activity_id)

        if data_filter.name:
            statement = statement.where(func.lower(OrganisationModel.name).like(f"%{data_filter.name.lower()}%"))

        result = (await session.execute(statement)).scalars().all()
        return [OrganisationListResponse(**elm.model_dump()) for elm in result]

    @staticmethod
    async def get_detail(session: AsyncSession, organisation_id: int) -> OrganisationDetailResponse:
        statement = (
            select(OrganisationModel)
            .options(selectinload(OrganisationModel.phones), selectinload(OrganisationModel.activities))
            .where(OrganisationModel.id == organisation_id)
        )
        result = (await session.execute(statement)).scalar_one_or_none()

        if not result:
            raise OrganisationNotFoundError(name="Organisation", _id=organisation_id)

        phones = [PhoneResponse(phone=phone.phone) for phone in result.phones]
        activities = [ActivityResponse(id=activity.activity_id) for activity in result.activities]

        return OrganisationDetailResponse(
            id=result.id,
            type=result.type,
            name=result.name,
            phones=phones,
            activities=activities,
        )


@lru_cache
def get_organisations_service() -> OrganisationsService:
    return OrganisationsService()


__all__ = [
    "get_organisations_service",
]
