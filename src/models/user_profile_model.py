from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class UserProfileDB(Base):
    __tablename__ = "user_profiles"

    name: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date)
    gender: Mapped[Optional[str]] = mapped_column(String(10))
    description: Mapped[Optional[str]] = mapped_column(String(300))
    user_id: Mapped[int] = mapped_column(unique=True)
    geo_location: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326, spatial_index=True)
    )

    @property
    def age(self) -> int:
        """
        Расчет текущего возраста в полных годах.
        """
        today = date.today()
        difference = relativedelta(today, self.date_of_birth)
        return difference.years
