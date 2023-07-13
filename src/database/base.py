from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase

__all__ = ('Base', 'init_tables')


class Base(DeclarativeBase):
    pass


def init_tables(engine: Engine) -> None:
    Base.metadata.create_all(engine)
