from aiogram import Dispatcher

from data.messages_config import USER_STATE_RESET
from keyboards.inline.activation_keyboard import activation_keyboard
from loader import db, dp
from states.permission import Permission


async def on_startup_state_setter(dp: Dispatcher):
    to_set_state = []
    records = await db.get_all_users()
    records = [dict(i) for i in records]
    for i in records:
        to_set_state.append(int(i.get('user_id')))
    for i in to_set_state:
        await dp.bot.send_message(i, USER_STATE_RESET,
                                  disable_notification=True, reply_markup=activation_keyboard)
        # print((await dp.bot.get_chat(419519710)))
        # await Permission.allowed.set()#TODO try to solve it
