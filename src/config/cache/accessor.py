from redis import asyncio as redis

from src.config.project_config import Settings

settings = Settings()


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host=settings.CACHE_HOST,
        port=settings.CACHE_PORT,
        db=settings.CACHE_DB,
    )
