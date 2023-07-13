from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert

from database import Department
from models import departments as department_models
from repositories.base import BaseRepository

__all__ = ('DepartmentRepository',)


class DepartmentRepository(BaseRepository):

    def get_all(self) -> list[department_models.Department]:
        statement = select(Department)
        with self._session_factory() as session:
            departments = session.scalars(statement).all()
        return [
            department_models.Department(
                id=department.id,
                name=department.name,
            ) for department in departments
        ]

    def create(self, department: department_models.Department):
        statement = (
            insert(Department)
            .values(
                id=department.id,
                name=department.name,
                quota=department.quota,
            )
            .on_conflict_do_nothing(index_elements=['id'])
        )
        with self._session_factory() as session:
            with session.begin():
                session.execute(statement)
