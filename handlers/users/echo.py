from aiogram import types

from data.messages_config import MESSAGE_FOR_NOT_AUTHORIZED_USERS
from loader import dp
from states.permission import Permission


@dp.message_handler(state=Permission.not_allowed)
async def echo(message: types.Message):
    await message.answer(MESSAGE_FOR_NOT_AUTHORIZED_USERS)
