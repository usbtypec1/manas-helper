import httpx

import models
from services.parsers import parse_ratings_page, parse_departments_page


async def get_ratings_page(
        *,
        http_client: httpx.AsyncClient,
        department_id: int,
) -> list[models.ApplicationRow]:
    url = (
        'https://abiturient.manas.edu.kg/page/index.php'
        f'?r=site%2Fmonitoring-dep&id={department_id}'
    )
    response = await http_client.get(url)
    return parse_ratings_page(department_id, response.text)


def get_departments() -> list[models.Department]:
    departments_page_url = (
        'https://abiturient.manas.edu.kg/page/index.php'
        '?r=site%2Fmonitoring-all-deps&lang=ru'
    )
    response = httpx.get(
        departments_page_url,
        timeout=30,
    )
    return parse_departments_page(response.text)
