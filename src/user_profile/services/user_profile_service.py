import hashlib
import json
from dataclasses import dataclass

from src.models.user_profile_model import UserProfileDB
from src.user_profile.cache.user_profile_cache import UserProfileCache
from src.user_profile.exceptions.user_profile_exceptions import (
    UserProfileExistsError,
    UserProfileNotFoundError,
)
from src.user_profile.repositories.user_profile_repository import UserProfileRepository
from src.user_profile.schemas.user_profile_schema import (
    UserProfileCreateSchema,
    UserProfileSchema,
    UserProfileUpdateSchema,
)


@dataclass
class UserProfileService:
    user_profile_repository: UserProfileRepository
    user_profile_cache: UserProfileCache

    async def get_user_profiles(
        self, user_id: int, radius: int, min_age: int, max_age: int
    ) -> list[UserProfileSchema]:
        current_profile = await self.get_user_profile_or_404(user_id)
        cache_key = self._generate_cache_key(
            user_id=user_id, radius=radius, min_age=min_age, max_age=max_age
        )

        if user_profiles := await self.user_profile_cache.get_cached_profiles(
            cache_key=cache_key
        ):
            return user_profiles

        user_profiles = await self.user_profile_repository.get_user_profiles(
            current_profile, radius, min_age, max_age
        )
        if user_profiles:
            user_profiles_schema = [
                UserProfileSchema.model_validate(user_profile)
                for user_profile in user_profiles
            ]
            await self.user_profile_cache.set_cached_profiles(
                cache_key=cache_key, user_profiles_schema=user_profiles_schema
            )
        return user_profiles

    async def create_user_profile(
        self, body: UserProfileCreateSchema, user_id: int
    ) -> UserProfileSchema:
        current_profile = (
            await self.user_profile_repository.get_user_profile_by_user_id(
                user_id=user_id
            )
        )

        if current_profile:
            raise UserProfileExistsError(user_id)

        profile_id = await self.user_profile_repository.create_user_profile(
            body=body, user_id=user_id
        )
        user_profile = await self.user_profile_repository.get_user_profile_by_id(
            profile_id
        )
        return UserProfileSchema.model_validate(user_profile)

    async def update_user_profile(
        self, body: UserProfileUpdateSchema, user_id: int
    ) -> UserProfileSchema:
        current_profile = await self.get_user_profile_or_404(user_id)
        user_profile = await self.user_profile_repository.update_user_profile(
            body=body, current_profile=current_profile
        )
        return UserProfileSchema.model_validate(user_profile)

    async def delete_user_profile(self, user_id: int) -> None:
        current_profile = await self.get_user_profile_or_404(user_id)
        await self.user_profile_repository.delete_user_profile(
            current_profile=current_profile
        )

    async def get_user_profile_or_404(self, user_id: int) -> UserProfileDB:
        if (
            current_profile
            := await self.user_profile_repository.get_user_profile_by_user_id(
                user_id=user_id
            )
        ):
            return current_profile

        raise UserProfileNotFoundError

    def _generate_cache_key(
        self, user_id: int, radius: int, min_age: int, max_age: int
    ) -> str:
        data = {
            "user_id": user_id,
            "radius": radius,
            "min_age": min_age,
            "max_age": max_age,
        }
        data_json = json.dumps(data, sort_keys=True)
        key = hashlib.sha256(data_json.encode()).hexdigest()
        return f"user_search:{key}"
