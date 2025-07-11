from dataclasses import dataclass

from geoalchemy2.functions import ST_DWithin
from sqlalchemy import and_, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_profile_model import UserProfileDB
from src.user_profile.schemas.user_profile_schema import (
    UserProfileCreateSchema,
    UserProfileUpdateSchema,
)


@dataclass
class UserProfileRepository:
    db_session: AsyncSession

    async def create_user_profile(
        self, body: UserProfileCreateSchema, user_id: int
    ) -> int:
        query = (
            insert(UserProfileDB)
            .values(
                name=body.name,
                gender=body.gender,
                date_of_birth=body.date_of_birth,
                description=body.description,
                user_id=user_id,
                geo_location=f"POINT({body.latitude} {body.longitude})",
            )
            .returning(UserProfileDB.id)
        )
        async with self.db_session as session:
            user_profile_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
        return user_profile_id

    async def get_user_profiles(
        self, current_profile: UserProfileDB, radius: int, min_age: int, max_age: int
    ) -> list[UserProfileDB]:
        async with self.db_session as session:
            user_profiles: list[UserProfileDB] = (
                (
                    await session.execute(
                        select(UserProfileDB).where(
                            and_(
                                ST_DWithin(
                                    UserProfileDB.geo_location,
                                    current_profile.geo_location,
                                    1 * radius,
                                ),
                                UserProfileDB.id != current_profile.id,
                            )
                        )
                    )
                )
                .scalars()
                .all()
            )
            user_profiles = [
                user_profile
                for user_profile in user_profiles
                if min_age <= user_profile.age <= max_age
            ]
            return user_profiles

    async def get_user_profile_by_id(
        self, user_profile_id: int
    ) -> UserProfileDB | None:
        query = select(UserProfileDB).where(UserProfileDB.id == user_profile_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_profile_by_user_id(self, user_id: int) -> UserProfileDB | None:
        query = select(UserProfileDB).where(UserProfileDB.user_id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def update_user_profile(
        self, body: UserProfileUpdateSchema, current_profile: UserProfileDB
    ) -> UserProfileDB:
        async with self.db_session as session:
            query = update(UserProfileDB).where(UserProfileDB.id == current_profile.id)

            updates = {}
            if body.description:
                updates["description"] = body.description
            if body.longitude and body.latitude:
                updates["geo_location"] = func.ST_SetSRID(
                    func.ST_MakePoint(body.longitude, body.latitude), 4326
                )

            if updates:
                query = query.values(**updates)
                await session.execute(query)
                await session.commit()

            return await self.get_user_profile_by_id(current_profile.id)

    async def delete_user_profile(self, current_profile: UserProfileDB) -> None:
        query = delete(UserProfileDB).where(UserProfileDB.id == current_profile.id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
