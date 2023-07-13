from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from repositories import ApplicationRepository

__all__ = ('register_handlers',)

from views import ApplicationsCountView
from views.applications_statistics import ApplicationExamScoresStatisticsView


async def on_show_applications_count(
        message: Message,
        application_repository: ApplicationRepository,
) -> None:
    applications_statistics = application_repository.aggregated_statistics_by_departments()
    view = ApplicationsCountView(applications_statistics)
    await message.reply(view.get_text())


async def on_show_exams_statistics(
        message: Message,
        application_repository: ApplicationRepository,
) -> None:
    applications_statistics = application_repository.aggregated_statistics_by_departments()
    view = ApplicationExamScoresStatisticsView(applications_statistics)
    await message.reply(view.get_text())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_applications_count,
        Command('applications_count'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_show_exams_statistics,
        Command('applications_statistics'),
        state='*',
    )
