from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# TODO: experement with it
from data.messages_config import PAID_KEYBOARD_UNDO, PAID_KEYBOARD_PAY, PAID_KEYBOARD_BUY, PURCHASE_INIT
from loader import bot


async def purchase_callback_factory(item_id: int, name):
    purchase = InlineKeyboardMarkup(row_width=2)
    bot_name = (await bot.me).username
    buy = InlineKeyboardButton(text=PAID_KEYBOARD_BUY.format(name), callback_data=f'buy{item_id}',
                               url=f'https://telegram.me/{bot_name}?start=buy{item_id}')
    purchase.insert(buy)
    return purchase


start_purchase_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=PURCHASE_INIT,
                callback_data="init")
        ],
    ]
)


paid_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=PAID_KEYBOARD_PAY,
                callback_data="paid")
        ],
        [
            InlineKeyboardButton(
                text=PAID_KEYBOARD_UNDO,
                callback_data="cancel")
        ],
    ]
)