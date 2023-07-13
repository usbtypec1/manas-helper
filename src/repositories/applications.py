from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert

import models
from database import Application, Department
from repositories.base import BaseRepository

__all__ = ('ApplicationRepository',)


class ApplicationRepository(BaseRepository):

    def create(self, application: models.ApplicationRow):
        statement = (
            insert(Application)
            .values(
                id=application.applicant_id,
                applied_at=application.applied_at,
                exams_score=application.exams_score,
                additional_score=application.additional_score,
                department_id=application.department_id,
            )
            .on_conflict_do_nothing(index_elements=('id',))
        )
        with self._session_factory() as session:
            with session.begin():
                session.execute(statement)

    def aggregated_statistics_by_departments(self):
        statement = (
            select(
                Department.name,
                func.count(Application.id),
                func.min(Application.exams_score),
                func.max(Application.exams_score),
                func.avg(Application.exams_score),
            )
            .join(
                Department,
                onclause=Application.department_id == Department.id,
            )
            .group_by(Application.department_id)
            .order_by(func.count(Application.id).desc())
        )
        with self._session_factory() as session:
            rows = session.execute(statement).all()
        return [
            models.ApplicationStatistics(
                department_name=department_name,
                applicants_count=applications_count,
                min_exams_score=min_exams_score,
                max_exams_score=max_exams_score,
                average_exams_score=average_exams_score,
            ) for department_name, applications_count,
            min_exams_score, max_exams_score, average_exams_score in rows
        ]
