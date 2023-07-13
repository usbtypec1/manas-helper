from collections.abc import Iterable

import models
from views.base import View

__all__ = ('ApplicationExamScoresStatisticsView',)


class ApplicationExamScoresStatisticsView(View):

    def __init__(
            self,
            applications_statistics: Iterable[models.ApplicationStatistics],
    ):
        self.__applications_statistics = applications_statistics

    def get_text(self) -> str:
        lines = ['<b>Факультет - мин | макс | сред (экз. осн. баллы)</b>']
        max_score = max(
            application_statistics_by_group.max_exams_score
            for application_statistics_by_group in
            self.__applications_statistics
        )
        min_score = max(
            application_statistics_by_group.min_exams_score
            for application_statistics_by_group in
            self.__applications_statistics
        )
        for application_statistics_by_group in self.__applications_statistics:
            lines.append(
                f'📍 {application_statistics_by_group.department_name}'
                f' - {application_statistics_by_group.min_exams_score}'
                f' | {application_statistics_by_group.max_exams_score}'
                f' | {application_statistics_by_group.average_exams_score:.2f}'
            )
            total_count += application_statistics_by_group.applicants_count
        lines.append(
            f'<b>Максимальный балл: {max_score}</b>\n'
            f'<b>Минимальный балл: {min_score}</b>'
        )
        return '\n'.join(lines)
