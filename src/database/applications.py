from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class Application(Base):
    __tablename__ = 'applications'
    id: Mapped[str] = mapped_column(primary_key=True)
    applied_at: Mapped[datetime]
    exams_score: Mapped[float]
    additional_score: Mapped[float]
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))

    department = relationship('Department', back_populates='applications')
