from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from repositories import ApplicationRepository

__all__ = ('register_handlers',)

from views import ApplicationsCountView


async def on_show_applications_count(
        message: Message,
        application_repository: ApplicationRepository,
) -> None:
    applications_by_departments = application_repository.count_by_departments()
    view = ApplicationsCountView(applications_by_departments)
    await message.reply(view.get_text())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_applications_count,
        Command('applications_count'),
        state='*',
    )
