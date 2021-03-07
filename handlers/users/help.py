from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from data.messages_config import MESSAGE_FOR_NOT_AUTHORIZED_USERS, HELP_FOR_AUTHORIZED_USERS
from loader import dp
from states.permission import Permission
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), state=Permission.allowed)
async def help(message: types.Message):
    await message.answer(HELP_FOR_AUTHORIZED_USERS)


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp(), state=Permission.not_allowed)
async def help(message: types.Message):
    await message.answer(MESSAGE_FOR_NOT_AUTHORIZED_USERS)