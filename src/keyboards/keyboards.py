from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.lexicon import Buttons


def admin_keyboard() -> InlineKeyboardMarkup:
    admin_keyboard_builder = InlineKeyboardBuilder()

    refresh_link_button = InlineKeyboardButton(
        text=Buttons.refresh_link,
        callback_data="refresh_link",
    )

    admin_keyboard_builder.row(refresh_link_button)

    return admin_keyboard_builder.as_markup()
