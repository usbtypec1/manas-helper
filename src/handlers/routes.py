from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text, CommandStart
from aiogram.types import (
    CallbackQuery, Message, ChatType,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from callback_data import ToggleRouteCallbackData
from repositories import RouteRepository, DepartmentRepository
from views.routes_menu import RoutesToggleMenuView

__all__ = ('register_handlers',)


async def on_show_toggle_menu(
        message: Message,
        route_repository: RouteRepository,
        department_repository: DepartmentRepository,
) -> None:
    department_ids = route_repository.get_department_ids_by_chat_id(
        message.chat.id)
    departments = department_repository.get_all()
    view = RoutesToggleMenuView(
        toggled_department_ids=department_ids,
        departments=departments,
    )
    await message.reply(
        text=view.get_text(),
        reply_markup=view.get_reply_markup()
    )


async def on_toggle_route(
        callback_query: CallbackQuery,
        callback_data: dict,
        route_repository: RouteRepository,
        department_repository: DepartmentRepository,
) -> None:
    chat_id = callback_query.message.chat.id
    department_id: int = callback_data['department_id']
    is_enabled = route_repository.is_enabled(chat_id, department_id)
    if is_enabled:
        route_repository.delete(chat_id, [department_id])
    else:
        route_repository.create(chat_id, [department_id])

    department_ids = route_repository.get_department_ids_by_chat_id(chat_id)
    departments = department_repository.get_all()
    view = RoutesToggleMenuView(
        toggled_department_ids=department_ids,
        departments=departments,
    )
    await callback_query.message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup()
    )


async def on_enable_all(
        callback_query: CallbackQuery,
        route_repository: RouteRepository,
        department_repository: DepartmentRepository,
) -> None:
    chat_id = callback_query.message.chat.id
    departments = department_repository.get_all()
    department_ids = [department.id for department in departments]
    route_repository.create(chat_id, department_ids)
    department_ids = route_repository.get_department_ids_by_chat_id(chat_id)
    view = RoutesToggleMenuView(
        toggled_department_ids=department_ids,
        departments=departments,
    )
    await callback_query.message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup()
    )


async def on_disable_all(
        callback_query: CallbackQuery,
        route_repository: RouteRepository,
        department_repository: DepartmentRepository,
) -> None:
    chat_id = callback_query.message.chat.id
    departments = department_repository.get_all()
    department_ids = [department.id for department in departments]
    route_repository.delete(chat_id, department_ids)
    department_ids = route_repository.get_department_ids_by_chat_id(chat_id)
    view = RoutesToggleMenuView(
        toggled_department_ids=department_ids,
        departments=departments,
    )
    await callback_query.message.edit_text(
        text=view.get_text(),
        reply_markup=view.get_reply_markup()
    )


async def on_settings_in_group(message: Message):
    me = await Dispatcher.get_current().bot.get_me()
    url = f'https://t.me/{me.username}?start=settings'
    await message.reply('Данный функционал работает только в ЛС', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('GO 🚀', url=url)
            ]
        ]
    ))


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_toggle_menu,
        Command('settings') | CommandStart(deep_link='settings'),
        state='*',
        chat_type=ChatType.PRIVATE
    )
    dispatcher.register_callback_query_handler(
        on_toggle_route,
        ToggleRouteCallbackData().filter(),
        state='*',
        chat_type=ChatType.PRIVATE,
    )
    dispatcher.register_callback_query_handler(
        on_enable_all,
        Text('enable-all'),
        state='*',
        chat_type=ChatType.PRIVATE,
    )
    dispatcher.register_callback_query_handler(
        on_disable_all,
        Text('disable-all'),
        state='*',
        chat_type=ChatType.PRIVATE,
    )
    dispatcher.register_message_handler(
        on_settings_in_group,
        Command('settings'),
        state='*',
        chat_type=[ChatType.GROUP, ChatType.SUPERGROUP],
    )
