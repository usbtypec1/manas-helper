from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

__all__ = ('Department',)


class Department(Base):
    __tablename__ = 'departments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str]

    applications = relationship('Application', back_populates='department')
