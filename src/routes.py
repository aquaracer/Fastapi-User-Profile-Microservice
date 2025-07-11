from fastapi import APIRouter

from src.user_profile.controllers.user_porfile_controller import (
    router as user_profile_router,
)


def get_apps_router():
    router = APIRouter()
    router.include_router(user_profile_router)
    return router
