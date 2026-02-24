from contextlib import asynccontextmanager
from random import choice, randint

from faker import Faker

from app.models.activities import ActivityModel
from app.models.buildings import BuildingModel, CityModel, StreetModel
from app.models.organisations import (
    OrganisationActivityModel,
    OrganisationAddressModel,
    OrganisationModel,
    OrganisationTypes,
    PhoneModel,
)
from app.pg import AsyncSession, get_session


async def load_activities(session: AsyncSession) -> list[ActivityModel]:
    fake = Faker()
    activities = []
    for _ in range(10):
        parent = ActivityModel(name=Faker().text(), parent_id=None)
        session.add(parent)
        activities.append(parent)
        await session.flush()
        for _ in range(3):
            child_1 = ActivityModel(
                name=fake.text(),
                parent_id=parent.id,
            )
            session.add(child_1)
            activities.append(child_1)
            await session.flush()
            for _ in range(3):
                child_2 = ActivityModel(
                    name=fake.text(),
                    parent_id=child_1.id,
                )
                session.add(child_2)
                activities.append(child_2)
    await session.commit()
    return activities


async def load_buildings(session: AsyncSession) -> list[BuildingModel]:
    fake = Faker()
    buildings = []
    for _ in range(10):
        city = CityModel(name=fake.city())
        session.add(city)
        await session.flush()
        for _ in range(100):
            street = StreetModel(name=fake.street_name(), city_id=city.id)
            session.add(street)
            await session.flush()
            for _ in range(20):
                building = BuildingModel(
                    name=fake.building_number(),
                    street_id=street.id,
                    latitude=fake.latitude(),
                    longitude=fake.longitude(),
                )
                session.add(building)
                buildings.append(building)
    await session.commit()
    return buildings


async def load_organisations(
    session: AsyncSession, activities: list[ActivityModel], buildings: list[BuildingModel]
) -> None:
    fake = Faker()
    for _ in range(100):
        office = OrganisationAddressModel(building_id=choice(buildings).id, office=fake.name())
        session.add(office)
        await session.flush()
        organisation = OrganisationModel(
            type=choice([ot.value for ot in OrganisationTypes]),
            name=fake.name(),
            address_id=office.id,
        )
        session.add(organisation)
        await session.flush()
        for _ in range(randint(0, 3)):
            phone = PhoneModel(
                phone=fake.phone_number()[:14],
                organisation_id=organisation.id,
            )
            session.add(phone)
        for _ in range(randint(0, 5)):
            org_activity = OrganisationActivityModel(
                organisation_id=organisation.id,
                activity_id=choice(activities).id,
            )
            session.add(org_activity)
    await session.commit()


async def load_fake_data() -> None:
    get_session_ctx = asynccontextmanager(get_session)
    async with get_session_ctx() as session:
        activities = await load_activities(session=session)
        buildings = await load_buildings(session=session)
        await load_organisations(session=session, activities=activities, buildings=buildings)
