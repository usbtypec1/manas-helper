from collections.abc import Iterable

import models
from views.base import View

__all__ = ('ApplicationsCountView',)


class ApplicationsCountView(View):

    def __init__(
            self,
            applications_count_by_departments: (
                    Iterable[models.ApplicationsCountByDepartment]
            ),
    ):
        self.__applications_count_by_departments = (
            applications_count_by_departments
        )

    def get_text(self) -> str:
        lines = ['<b>Факультет - количество людей | квота на факультет</b>']
        total_count = 0
        total_quota = 0
        for department_applications in self.__applications_count_by_departments:
            has_positions = department_applications.count < department_applications.quota
            icon = '☘️' if has_positions else '❌'
            lines.append(
                f'📍 {department_applications.department_name}'
                f' - {department_applications.count}'
                f' | {department_applications.quota} {icon}'
            )
            total_count += department_applications.count
            total_quota += department_applications.quota
        lines.append(f'<b>Общее количество: {total_count}'
                     f' | {total_quota}</b>')
        return '\n'.join(lines)
