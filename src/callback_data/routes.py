from aiogram.utils.callback_data import CallbackData

__all__ = ('ToggleRouteCallbackData',)


class ToggleRouteCallbackData(CallbackData):

    def __init__(self):
        super().__init__('toggle-route', 'department_id')

    def parse(self, callback_data: str) -> dict:
        callback_data = super().parse(callback_data)
        return {'department_id': int(callback_data['department_id'])}
