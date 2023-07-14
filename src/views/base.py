from typing import TypeAlias

from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)

__all__ = ('View', 'ReplyMarkup')

ReplyMarkup: TypeAlias = (
        InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
)


class View:
    text: str | None = None
    reply_markup: ReplyMarkup | None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup
