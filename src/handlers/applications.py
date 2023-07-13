from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from repositories import ApplicationRepository, DepartmentRepository
from services.applications import (
    group_by_department_name,
    compute_applications_statistics
)
from views import ApplicationsCountView
from views.applications_statistics import ApplicationExamScoresStatisticsView

__all__ = ('register_handlers',)


async def on_show_applications_count(
        message: Message,
        application_repository: ApplicationRepository,
) -> None:
    applications_statistics = application_repository.count_by_departments()
    view = ApplicationsCountView(applications_statistics)
    await message.reply(view.get_text())


async def on_show_exams_statistics(
        message: Message,
        department_repository: DepartmentRepository,
        application_repository: ApplicationRepository,
) -> None:
    departments = department_repository.get_all()
    rows = []
    for department in departments:
        rows += application_repository.aggregated_statistics_by_department(
            department_id=department.id,
            limit=department.quota,
        )
    stats = compute_applications_statistics(group_by_department_name(rows))
    view = ApplicationExamScoresStatisticsView(stats)
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
