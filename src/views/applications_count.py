from views.base import View

__all__ = ('ApplicationsCountView',)


class ApplicationsCountView(View):

    def __init__(self, applications_count_by_departments):
        self.__applications_count_by_departments = (
            applications_count_by_departments
        )

    def get_text(self) -> str:
        lines = ['<b>Факультет - количество людей</b>']
        total_count = 0
        for department, applications_count in (
                self.__applications_count_by_departments
        ):
            lines.append(f'📍 {department} - {applications_count}')
            total_count += applications_count
        lines.append(f'<b>Общее количество: {total_count}</b>')
        return '\n'.join(lines)
