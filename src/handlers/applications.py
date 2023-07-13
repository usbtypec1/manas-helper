from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from repositories import ApplicationRepository

__all__ = ('register_handlers',)


async def on_show_applications_count(
        message: Message,
        application_repository: ApplicationRepository,
) -> None:
    applications_count = application_repository.count()
    await message.reply(
        f'Уже <b>{applications_count}</b> человек кинули свои талоны'
    )


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_applications_count,
        Command('applications_count'),
        state='*',
    )
