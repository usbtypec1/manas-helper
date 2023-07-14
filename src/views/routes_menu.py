from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from callback_data import ToggleRouteCallbackData
from views.base import View

__all__ = ('RoutesToggleMenuView',)


class RoutesToggleMenuView(View):
    text = 'Выберите факультеты, по которым вы хотите получать уведомления'

    def __init__(
            self,
            *,
            toggled_department_ids: Iterable[int],
            departments: Iterable[models.Department],
    ):
        self.__toggled_department_ids = set(toggled_department_ids)
        self.__departments = tuple(departments)

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        for department in self.__departments:
            is_enabled = '💚' if department.id in self.__toggled_department_ids else '❤️'
            markup.insert(
                InlineKeyboardButton(
                    text=f'{is_enabled} {department.name}',
                    callback_data=ToggleRouteCallbackData().new(
                        department_id=department.id,
                    ),
                )
            )
        markup.row(
            InlineKeyboardButton('Включить все', callback_data='enable-all'),
            InlineKeyboardButton('Выключить все', callback_data='disable-all'),
        )
        return markup
