from datetime import datetime

from bs4 import BeautifulSoup

import models


def parse_ratings_page(
        department_id: int,
        html: str,
) -> list[models.ApplicationRow]:
    soup = BeautifulSoup(html, 'lxml')
    applications: list[models.ApplicationRow] = []
    for tr in soup.find('table').find_all('tr')[1:]:
        tds = tr.find_all('td')
        rating = int(tds[0].text)
        applicant_id = tds[1].text
        exams_score = float(tds[2].text)
        additional_score = float(tds[3].text)
        applied_at = datetime.strptime(tds[4].text, '%d/%m/%Y %H:%M:%S')
        applications.append(models.ApplicationRow(
            department_id=department_id,
            applied_at=applied_at,
            rating=rating,
            applicant_id=applicant_id,
            exams_score=exams_score,
            additional_score=additional_score,
        ))
    return applications


def parse_departments_page(html: str) -> list[models.Department]:
    departments: list[models.Department] = []

    table = BeautifulSoup(html, 'lxml')
    for a in table.find_all('a'):
        if 'monitoring-dep' in a.get('href'):
            department_id = int(a.get('href').split('id=')[-1])
            department_name = a.text

            departments.append(
                models.Department(
                    id=department_id,
                    name=department_name,
                ),
            )
    return departments
