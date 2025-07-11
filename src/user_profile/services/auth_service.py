import datetime as dt
from dataclasses import dataclass

from jose import JWTError, jwt

from src.config.project_config import Settings
from src.user_profile.exceptions.user_profile_exceptions import (
    TokenExpiredError,
    TokenIsNotCorrectError,
)


@dataclass
class AuthService:
    settings: Settings

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                access_token,
                self.settings.JWT_SECRET_KEY,
                algorithms=[self.settings.JWT_ENCODE_ALGORITHM],
            )
        except JWTError:
            raise TokenIsNotCorrectError from JWTError
        if payload["expire"] < dt.datetime.utcnow().timestamp():
            raise TokenExpiredError
        return payload["user_id"]
