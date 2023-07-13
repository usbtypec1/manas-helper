from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert

import models
from database import Application
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

    def count(self) -> int:
        statement = select(func.count(Application.id))
        with self._session_factory() as session:
            row = session.execute(statement).first()
        return 0 if row is None else row[0]
