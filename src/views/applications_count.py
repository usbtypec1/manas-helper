from collections.abc import Iterable

import models
from views.base import View

__all__ = ('ApplicationsCountView',)


class ApplicationsCountView(View):

    def __init__(
            self,
            applications_statistics: Iterable[models.ApplicationStatistics],
    ):
        self.__applications_statistics = applications_statistics

    def get_text(self) -> str:
        lines = ['<b>Факультет - количество людей</b>']
        total_count = 0
        for application_statistics_by_group in self.__applications_statistics:
            lines.append(
                f'📍 {application_statistics_by_group.department_name}'
                f' - {application_statistics_by_group.applicants_count}'
            )
            total_count += application_statistics_by_group.applicants_count
        lines.append(f'<b>Общее количество: {total_count}</b>')
        return '\n'.join(lines)
