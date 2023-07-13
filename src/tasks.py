import asyncio

import httpx

from repositories import DepartmentRepository, ApplicationRepository
from services.manas import get_ratings_page


async def make_snapshot(
        department_repository: DepartmentRepository,
        application_repository: ApplicationRepository,
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
            application_repository.create(
                department_id=department_rating.department.id,
                application=application,
            )
