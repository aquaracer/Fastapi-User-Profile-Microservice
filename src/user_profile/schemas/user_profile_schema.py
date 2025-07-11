from datetime import date

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, PositiveInt, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude


class UserProfileSchema(BaseModel):
    id: int | None = None
    name: str | None = None
    gender: str | None = None
    age: PositiveInt | None = None
    description: str | None = None
    user_id: int | None = None

    class Config:
        from_attributes = True


class UserProfileCreateSchema(BaseModel):
    name: str
    gender: str
    date_of_birth: date
    description: str | None = None
    user_id: int
    latitude: Latitude
    longitude: Longitude

    @field_validator("date_of_birth")
    @classmethod
    def validate_age_minimum(cls, dob: date) -> date:
        """
        Валидирует, что пользователь достиг минимального возраста (18 лет)
        и что дата рождения не находится в будущем.
        """
        today = date.today()

        if dob > today:
            raise ValueError("The date of birth cannot be in the future")

        age = relativedelta(today, dob).years
        if age < 18:
            raise ValueError(
                "Registration is allowed only for users 18 years or older"
            )
        return dob


class Config:
    from_attributes = True


class UserProfileUpdateSchema(BaseModel):
    description: str | None = None
    latitude: Latitude | None = None
    longitude: Longitude | None = None

    class Config:
        from_attributes = True
