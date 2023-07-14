from collections.abc import Iterable

import models
from views.base import View

__all__ = ('TopApplicationsView',)


class TopApplicationsView(View):

    def __init__(self, applications: Iterable[models.Application]):
        self.__applications = applications

    def get_text(self) -> str:
        lines = [
            '<b>Топ абитуриентов (позиция | рег.номер | кол-во баллов | факультет)</b>']
        for num, application in enumerate(self.__applications, start=1):
            lines.append(
                f'<b>{num}</b> | №{application.applicant_id}'
                f' | {application.exams_score} |'
                f' <a href="https://abiturient.manas.edu.kg/page/index.php?r=site%2Fmonitoring-dep&id={application.department_id}">{application.department_name}</a>'
            )
        return '\n'.join(lines)
