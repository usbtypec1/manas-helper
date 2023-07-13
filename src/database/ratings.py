from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

__all__ = ('ApplicationRatings',)


class ApplicationRatings(Base):
    __tablename__ = 'application_ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[str] = mapped_column(ForeignKey('applications.id'))
    rating: Mapped[int]
    recorded_at: Mapped[datetime]

    __table_args__ = (
        UniqueConstraint('applicant_id', 'rating'),
    )
