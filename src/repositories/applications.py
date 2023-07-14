from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert

import models
from database import Application, Department
from repositories.base import BaseRepository

__all__ = ('ApplicationRepository',)


class ApplicationRepository(BaseRepository):

    def create(self, department_id: int,
               application: models.ApplicationRow) -> bool:
        statement = (
            insert(Application)
            .values(
                id=application.applicant_id,
                applied_at=application.applied_at,
                exams_score=application.exams_score,
                additional_score=application.additional_score,
                department_id=department_id,
            )
            .on_conflict_do_nothing(index_elements=('id',))
        )
        with self._session_factory() as session:
            with session.begin():
                result = session.execute(statement)
        return bool(result.rowcount)

    def count_by_departments(
            self,
    ) -> list[models.ApplicationsCountByDepartment]:
        statement = (
            select(
                Department.name,
                func.count(Application.id),
                Department.quota,
            )
            .join(
                Department,
                onclause=Application.department_id == Department.id,
            )
            .group_by(Application.department_id)
            .order_by(Department.name.asc())
        )
        with self._session_factory() as session:
            rows = session.execute(statement).all()
        return [
            models.ApplicationsCountByDepartment(
                department_name=department_name,
                count=applications_count,
                quota=quota,
            ) for department_name, applications_count, quota in rows
        ]

    def aggregated_statistics_by_department(
            self,
            department_id: int,
            *,
            limit: int | None = None,
    ) -> tuple[tuple[str, float], ...]:
        select()
        statement = (
            select(
                Department.name,
                Application.exams_score,
            )
            .where(Department.id == department_id)
            .join(
                Department,
                onclause=Application.department_id == Department.id,
            )
            .order_by(Application.exams_score.desc())
        )
        if limit is not None:
            statement = statement.limit(limit)
        with self._session_factory() as session:
            rows = session.execute(statement).all()
        return rows
