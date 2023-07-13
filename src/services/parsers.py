from datetime import datetime

from bs4 import BeautifulSoup

import models


def parse_quota_in_ratings_page(soup: BeautifulSoup) -> int:
    for p in soup.find_all('p'):
        if 'КВОТА' in p.text:
            parts = p.text.strip().split('КВОТА: ')
            if not parts:
                continue
            quota = parts[-1]
            if not quota.isdigit():
                continue
            return int(quota)

    raise ValueError('Quota number is not found in ratings page')


def parse_rating_rows(soup: BeautifulSoup) -> list[models.ApplicationRow]:
    applications: list[models.ApplicationRow] = []
    for tr in soup.find('table').find_all('tr')[1:]:
        tds = tr.find_all('td')
        rating = int(tds[0].text)
        applicant_id = tds[1].text
        exams_score = float(tds[2].text)
        additional_score = float(tds[3].text)
        applied_at = datetime.strptime(tds[4].text, '%d/%m/%Y %H:%M:%S')
        applications.append(models.ApplicationRow(
            applied_at=applied_at,
            rating=rating,
            applicant_id=applicant_id,
            exams_score=exams_score,
            additional_score=additional_score,
        ))
    return applications


def parse_ratings_page(
        department: models.DepartmentIDAndName,
        html: str,
) -> models.DepartmentRatings:
    soup = BeautifulSoup(html, 'lxml')
    rows = parse_rating_rows(soup)
    quota = parse_quota_in_ratings_page(soup)
    return models.DepartmentRatings(
        department=models.Department(
            id=department.id,
            name=department.name,
            quota=quota,
        ),
        application_rows=rows,
    )


def parse_departments_page(html: str) -> list[models.DepartmentIDAndName]:
    departments: list[models.DepartmentIDAndName] = []

    table = BeautifulSoup(html, 'lxml')
    for a in table.find_all('a'):
        if 'monitoring-dep' in a.get('href'):
            department_id = int(a.get('href').split('id=')[-1])
            department_name = a.text

            departments.append(
                models.DepartmentIDAndName(
                    id=department_id,
                    name=department_name,
                ),
            )
    return departments
