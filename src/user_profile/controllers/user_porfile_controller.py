import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.user_profile.cache.user_profile_cache import UserProfileCache
from src.user_profile.dependencies.user_profile_dependency import (
    get_request_user_id,
    get_user_profile_service,
)
from src.user_profile.exceptions.user_profile_exceptions import (
    UserProfileExistsError,
    UserProfileNotFoundError,
)
from src.user_profile.schemas.user_profile_schema import (
    UserProfileCreateSchema,
    UserProfileSchema,
    UserProfileUpdateSchema,
)
from src.user_profile.services.user_profile_service import UserProfileService

router = APIRouter(prefix="/user_profile", tags=["user_profile"])


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

@router.post("", response_model=UserProfileSchema)
async def create_user_profile(
        body: UserProfileCreateSchema,
        user_profile_service: Annotated[
            UserProfileService,
            Depends(get_user_profile_service)
        ],
        user_id: int = Depends(get_request_user_id),
):
    """Создание профиля пользователя"""
    try:
        logger.info(f"Hello from User Profile!")
        return await user_profile_service.create_user_profile(
            body=body, user_id=user_id
        )
    except UserProfileExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error.detail
        ) from error


@router.get("/list", response_model=list[UserProfileSchema])
async def get_user_profiles_with_filtering(
        user_profile_service: Annotated[
            UserProfileService,
            UserProfileCache,
            Depends(get_user_profile_service)
        ],
        radius: int,
        min_age: int,
        max_age: int,
        user_id: int = Depends(get_request_user_id),
):
    """Cписок профилей в заданном радиусе и диапазоне возрастов от текущего профиля"""
    try:
        return await user_profile_service.get_user_profiles(
            radius=radius,
            min_age=min_age,
            max_age=max_age,
            user_id=user_id,
        )
    except UserProfileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error.detail
        ) from error


@router.patch("", response_model=UserProfileSchema)
async def patch_user_profile(
        body: UserProfileUpdateSchema,
        user_profile_service: Annotated[
            UserProfileService,
            Depends(get_user_profile_service)
        ],
        user_id: int = Depends(get_request_user_id),
):
    """Изменения данных в профиле пользователя"""
    try:
        return await user_profile_service.update_user_profile(
            body=body, user_id=user_id
        )
    except UserProfileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error.detail
        ) from error


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
        user_profile_service: Annotated[
            UserProfileService,
            Depends(get_user_profile_service)
        ],
        user_id: int = Depends(get_request_user_id),
):
    """Удаление профиля"""
    try:
        await user_profile_service.delete_user_profile(user_id=user_id)
    except UserProfileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=error.detail
        ) from error
