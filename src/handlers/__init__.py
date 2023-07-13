from aiogram import Dispatcher

from . import applications

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    applications.register_handlers(dispatcher)
