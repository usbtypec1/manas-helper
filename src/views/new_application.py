import models
from views.base import View


class NewApplicationView(View):

    def __init__(
            self,
            *,
            department: models.Department,
            application: models.ApplicationRow,
    ):
        self.__department = department
        self.__application = application

    def get_text(self) -> str:
        beat_quota = '🔥' if self.__application.rating <= self.__department.quota else ''
        return (
            f'<b>❗️ Обнаружен новый талон</b>\n'
            f'<b>Рег. номер:</b> {self.__application.applicant_id}\n'
            f'<b>Факультет:</b> {self.__department.name}\n'
            f'<b>Время подачи:</b> {self.__application.applied_at:%H:%M:%S}\n'
            f'<b>Баллы:</b> {self.__application.exams_score}\n'
            f'<b>Рейтинг:</b> {self.__application.rating} {beat_quota}\n'
        )
