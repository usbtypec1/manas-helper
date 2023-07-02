import os
from datetime import datetime
from zoneinfo import ZoneInfo

import humanize
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import BotCommand, Message, ChatType
from aiogram.utils import executor

BISHKEK_TIMEZONE = ZoneInfo('Asia/Bishkek')
EXAMS_START_AT = datetime(2023, 7, 9, 10, tzinfo=BISHKEK_TIMEZONE)


def get_now() -> datetime:
    return datetime.now(BISHKEK_TIMEZONE)


async def on_show_last_time(message: Message) -> None:
    last_time = EXAMS_START_AT - get_now()
    humanized_last_time = humanize.precisedelta(
        last_time,
        minimum_unit='minutes',
        format='%0.0f',
    )
    text = f'До экзаменов осталось {humanized_last_time}'
    await message.answer(text)


async def setup_commands(dispatcher: Dispatcher) -> None:
    await dispatcher.bot.set_my_commands([
        BotCommand('exams', '😱 Оставшееся время до экзамена'),
    ])


def main():
    humanize.i18n.activate("ru_RU")
    bot = Bot(os.getenv('BOT_TOKEN'))
    dispatcher = Dispatcher(bot)
    dispatcher.register_message_handler(
        on_show_last_time,
        Command('exams') | Text(contains='экз', ignore_case=True),
        chat_type=[ChatType.PRIVATE, ChatType.GROUP, ChatType.SUPERGROUP]
    )
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=setup_commands,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
