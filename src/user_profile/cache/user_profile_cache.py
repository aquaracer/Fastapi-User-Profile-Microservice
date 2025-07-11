import json
from dataclasses import dataclass

from redis import asyncio as Redis

from src.user_profile.schemas.user_profile_schema import UserProfileSchema


@dataclass
class UserProfileCache:
    redis: Redis

    async def get_cached_profiles(self, cache_key: str) -> list[UserProfileSchema]:
        async with self.redis as redis:
            user_profiles_json = await redis.lrange(cache_key, 0, -1)
            return [
                UserProfileSchema.model_validate(json.loads(user_profile))
                for user_profile in user_profiles_json
            ]

    async def set_cached_profiles(
        self, cache_key: str, user_profiles_schema: list[UserProfileSchema]
    ) -> None:
        user_profile_json = [
            user_profile_schema.json() for user_profile_schema in user_profiles_schema
        ]
        async with self.redis as redis:
            await redis.lpush(cache_key, *user_profile_json)
