import httpx
from fastapi import Depends, HTTPException, Security, security, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.cache import get_redis_connection
from src.config.database import get_db_session
from src.config.project_config import Settings
from src.user_profile.cache.user_profile_cache import UserProfileCache
from src.user_profile.exceptions.user_profile_exceptions import (
    TokenExpiredError,
    TokenIsNotCorrectError,
)
from src.user_profile.repositories.user_profile_repository import UserProfileRepository
from src.user_profile.services.auth_service import AuthService
from src.user_profile.services.user_profile_service import UserProfileService


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_user_profile_repository(
        db_session: AsyncSession = Depends(get_db_session),
) -> UserProfileRepository:
    return UserProfileRepository(db_session=db_session)


async def get_user_profile_cache_repository() -> UserProfileCache:
    redis_connection = get_redis_connection()
    return UserProfileCache(redis_connection)


async def get_user_profile_service(
        user_profile_repository: UserProfileRepository = Depends(
            get_user_profile_repository
        ),
        user_profile_cache: UserProfileCache = Depends(
            get_user_profile_cache_repository
        ),
) -> UserProfileService:
    return UserProfileService(
        user_profile_repository=user_profile_repository,
        user_profile_cache=user_profile_cache,
    )


async def get_auth_service() -> AuthService:
    return AuthService(settings=Settings())


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpiredError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=error.detail
        ) from error

    except TokenIsNotCorrectError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=error.detail
        ) from error

    return user_id
