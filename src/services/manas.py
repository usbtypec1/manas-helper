import httpx

import models
from services.parsers import parse_ratings_page


async def get_ratings_page(
        *,
        http_client: httpx.AsyncClient,
        department: models.DepartmentIDAndName,
) -> models.DepartmentRatings:
    url = (
        'https://abiturient.manas.edu.kg/page/index.php'
        f'?r=site%2Fmonitoring-dep&id={department.id}'
    )
    response = await http_client.get(url)
    return parse_ratings_page(department, response.text)
