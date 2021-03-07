from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.messages_config import CONFIRMATION_KEYBOARD_YES, CONFIRMATION_KEYBOARD_NO

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=CONFIRMATION_KEYBOARD_YES, callback_data="ok"),
        InlineKeyboardButton(text=CONFIRMATION_KEYBOARD_NO, callback_data="not"),
    ]
])