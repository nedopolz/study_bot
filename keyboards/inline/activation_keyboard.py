from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.messages_config import ACTIVATION_KEYBOARD

activation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=ACTIVATION_KEYBOARD, callback_data="start"),
    ]
])