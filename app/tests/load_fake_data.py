from contextlib import asynccontextmanager
from random import choice, randint

from faker import Faker

from app.models.activities import ActivityModel
from app.models.organisations import OrganisationActivityModel, OrganisationModel, OrganisationTypes, PhoneModel
from app.pg import AsyncSession, get_session


async def load_activities(session: AsyncSession) -> list[ActivityModel]:
    activities = []
    for _ in range(10):
        parent = ActivityModel(name=Faker().text(), parent_id=None)
        session.add(parent)
        activities.append(parent)
        await session.flush()
        for _ in range(3):
            child_1 = ActivityModel(
                name=Faker().text(),
                parent_id=parent.id,
            )
            session.add(child_1)
            activities.append(child_1)
            await session.flush()
            for _ in range(3):
                child_2 = ActivityModel(
                    name=Faker().text(),
                    parent_id=child_1.id,
                )
                session.add(child_2)
                activities.append(child_2)
    await session.commit()
    return activities


async def load_organisations(session: AsyncSession, activities: list[ActivityModel]) -> None:
    for _ in range(100):
        organisation = OrganisationModel(
            type=choice([ot.value for ot in OrganisationTypes]),
            name=Faker().name(),
        )
        session.add(organisation)
        await session.flush()
        for _ in range(randint(0, 3)):
            phone = PhoneModel(
                phone=Faker().phone_number()[:14],
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
        await load_organisations(session=session, activities=activities)
