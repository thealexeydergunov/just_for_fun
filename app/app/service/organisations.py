from decimal import Decimal
from functools import lru_cache

from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import func, select, union_all

from app.exceptions import OrganisationNotFoundError
from app.models.activities import ActivityModel
from app.models.buildings import BuildingModel, StreetModel
from app.models.organisations import (
    ActivityResponseModel,
    OrganisationActivityModel,
    OrganisationAddressModel,
    OrganisationDetailResponseModel,
    OrganisationFilterModel,
    OrganisationListResponseModel,
    OrganisationModel,
    PhoneResponseModel,
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

    @staticmethod
    def _filter_by_building_id(statement, building_id: int):  # noqa: ANN205, ANN001
        statement = statement.where(OrganisationAddressModel.building_id == building_id)
        return statement

    @staticmethod
    def _filter_by_latitude_longitude(  # noqa: ANN205
        statement,  # noqa: ANN001
        latitude_from: Decimal,
        latitude_to: Decimal,
        longitude_from: Decimal,
        longitude_to: Decimal,
    ):
        statement = statement.where(
            BuildingModel.latitude.between(latitude_from, latitude_to),
            BuildingModel.longitude.between(longitude_from, longitude_to),
        )
        return statement

    async def get_list(
        self, session: AsyncSession, data_filter: OrganisationFilterModel
    ) -> list[OrganisationListResponseModel]:
        statement = select(OrganisationModel)
        if data_filter.latitude_from:
            statement = statement.join(OrganisationAddressModel).join(
                BuildingModel, OrganisationAddressModel.building_id == BuildingModel.id
            )
        elif data_filter.building_id:
            statement = statement.join(OrganisationAddressModel)

        if data_filter.building_id:
            statement = self._filter_by_building_id(statement=statement, building_id=data_filter.building_id)

        if data_filter.latitude_from:
            statement = self._filter_by_latitude_longitude(
                statement=statement,
                latitude_from=data_filter.latitude_from,
                latitude_to=data_filter.latitude_to,
                longitude_from=data_filter.longitude_from,
                longitude_to=data_filter.longitude_to,
            )

        if data_filter.activity_id:
            statement = self._filter_by_activity_id(statement=statement, activity_id=data_filter.activity_id)

        if data_filter.name:
            statement = statement.where(func.lower(OrganisationModel.name).like(f"%{data_filter.name.lower()}%"))

        result = (await session.execute(statement)).scalars().all()
        return [OrganisationListResponseModel(**elm.model_dump()) for elm in result]

    @staticmethod
    async def get_detail(session: AsyncSession, organisation_id: int) -> OrganisationDetailResponseModel:
        statement = (
            select(OrganisationModel)
            .options(
                selectinload(OrganisationModel.phones),
                selectinload(OrganisationModel.activities),
                joinedload(OrganisationModel.address)
                .joinedload(OrganisationAddressModel.building)
                .joinedload(BuildingModel.street)
                .joinedload(StreetModel.city),
            )
            .where(OrganisationModel.id == organisation_id)
        )
        result = (await session.execute(statement)).scalar_one_or_none()

        if not result:
            raise OrganisationNotFoundError(name="Organisation", _id=organisation_id)

        phones = [PhoneResponseModel(phone=phone.phone) for phone in result.phones]
        activities = [ActivityResponseModel(id=activity.activity_id) for activity in result.activities]
        return OrganisationDetailResponseModel(
            id=result.id,
            type=result.type,
            name=result.name,
            address=f"{result.address.building.street.city.name}, "
            f"{result.address.building.street.name}, "
            f"{result.address.building.name}, "
            f"{result.address.office}",
            phones=phones,
            activities=activities,
        )


@lru_cache
def get_organisations_service() -> OrganisationsService:
    return OrganisationsService()


__all__ = [
    "get_organisations_service",
]
