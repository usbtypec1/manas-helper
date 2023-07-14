from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base

__all__ = ('Route',)


class Route(Base):
    __tablename__ = 'routes'

    department_id: Mapped[int] = mapped_column(
        ForeignKey('departments.id'),
        primary_key=True,
    )
    chat_id: Mapped[int] = mapped_column(primary_key=True)
