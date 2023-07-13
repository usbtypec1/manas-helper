import asyncio

import httpx

from repositories import DepartmentRepository
from services.manas import get_ratings_page
from services.parsers import parse_departments_page

__all__ = ('init_departments',)


async def init_departments(
        department_repository: DepartmentRepository,
) -> None:
    excluded_departments = {
        'Живопись (Изобразительное искусство)',
        'Графика (Изобразительное искусство)',
        'Театральное искусство',
        'Музыкальное искусство',
        'Физическая культура',
        'Подготовка тренеров',
    }

    async with httpx.AsyncClient(timeout=60) as http_client:
        departments_page_url = (
            'https://abiturient.manas.edu.kg/page/index.php'
            '?r=site%2Fmonitoring-all-deps&lang=ru'
        )
        response = await http_client.get(departments_page_url)
        departments = parse_departments_page(response.text)

        async with asyncio.TaskGroup() as task_group:
            tasks = [
                task_group.create_task(
                    get_ratings_page(
                        http_client=http_client,
                        department=department,
                    )
                ) for department in departments
                if department.name not in excluded_departments
            ]

        departments_ratings = [task.result() for task in tasks]
        for department_ratings in departments_ratings:
            department_repository.create(department_ratings.department)
