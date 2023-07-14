from collections.abc import Iterable

from sqlalchemy import select, delete
from sqlalchemy.dialects.sqlite import insert

from database import Route
from repositories.base import BaseRepository

__all__ = ('RouteRepository',)


class RouteRepository(BaseRepository):

    def is_enabled(self, chat_id: int, department_id: int) -> bool:
        statement = select(Route).where(
            Route.chat_id == chat_id,
            Route.department_id == department_id
        )
        with self._session_factory() as session:
            return bool(session.execute(statement).first())

    def create(self, chat_id: int, department_ids: Iterable[int]):
        with self._session_factory() as session:
            with session.begin():
                for department_id in department_ids:
                    statement = (
                        insert(Route)
                        .values(chat_id=chat_id, department_id=department_id)
                        .on_conflict_do_nothing(
                            index_elements=['chat_id', 'department_id'])
                    )
                    session.execute(statement)

    def delete(self, chat_id: int, department_ids: Iterable[int]):
        statement = (
            delete(Route)
            .where(Route.department_id.in_(department_ids),
                   Route.chat_id == chat_id)
        )
        with self._session_factory() as session:
            with session.begin():
                session.execute(statement)

    def get_department_ids_by_chat_id(self, chat_id: int) -> list[int]:
        statement = select(Route.department_id).where(Route.chat_id == chat_id)
        with self._session_factory() as session:
            rows = session.execute(statement).all()
        return [row[0] for row in rows]

    def get_chat_ids_by_department_id(self, department_id: int) -> list[int]:
        statement = (
            select(Route.chat_id)
            .where(Route.department_id == department_id)
        )
        with self._session_factory() as session:
            rows = session.execute(statement).all()
        return [row[0] for row in rows]
