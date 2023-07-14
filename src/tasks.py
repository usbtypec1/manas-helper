import asyncio

import httpx
from aiogram import Bot
from aiogram.utils.exceptions import TelegramAPIError

from repositories import (
    DepartmentRepository, ApplicationRepository,
    RouteRepository
)
from services.manas import get_ratings_page
from views.new_application import NewApplicationView


async def make_snapshot(
        bot: Bot,
        department_repository: DepartmentRepository,
        application_repository: ApplicationRepository,
        route_repository: RouteRepository,
) -> None:
    departments = department_repository.get_all()

    async with httpx.AsyncClient(timeout=60) as http_client:
        async with asyncio.TaskGroup() as task_group:
            tasks = [
                task_group.create_task(
                    get_ratings_page(
                        department=department,
                        http_client=http_client,
                    )
                ) for department in departments
            ]

    for task in tasks:
        department_rating = task.result()
        for application in department_rating.application_rows:
            is_created = application_repository.create(
                department_id=department_rating.department.id,
                application=application,
            )

            if is_created:
                view = NewApplicationView(
                    department=department_rating.department,
                    application=application,
                )
                text = view.get_text()

                chat_ids = route_repository.get_chat_ids_by_department_id(
                    department_rating.department.id
                )
                try:
                    await bot.send_message(-1001551198132, text,
                                           message_thread_id=261318)
                except TelegramAPIError:
                    pass
                finally:
                    await asyncio.sleep(0.5)

                for chat_id in chat_ids:
                    try:
                        await bot.send_message(chat_id, text)
                    except TelegramAPIError:
                        pass
                    finally:
                        await asyncio.sleep(0.5)
