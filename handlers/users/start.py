import re

import asyncio
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.config import referal_bonus
from data.messages_config import MESSAGE_FOR_NOT_AUTHORIZED_USERS, WELCOME, ERORR_LINK, HI_USER, CODE_IS_NOT_NUMBER, \
    BAD_CODE, ON_STURTUP_READY
from loader import dp, db
from states.permission import Permission
from utils.user_check import user_checker


@dp.message_handler(CommandStart(deep_link=re.compile(r'^[0-9]{4,15}$')), state=Permission.not_allowed)
async def start_second_deeplink(message: types.Message):
    code = int(message.get_args())
    if await user_checker(code):
        await db.add_user(message.from_user.id)
        await db.add_bonus(message.from_user.id, 1)#TODO this just add some bonus to show
        await db.add_bonus(code, referal_bonus)
        await message.answer(WELCOME.format(message.from_user.full_name))
        await Permission.allowed.set()
    else:
        await message.answer(ERORR_LINK.format(message.from_user.full_name))
        await Permission.not_allowed.set()


@dp.message_handler(CommandStart(deep_link=re.compile(r'^[0-9]{4,15}$')))
async def start_first_deeplink(message: types.Message):
    code = int(message.get_args())
    if await user_checker(code):
        await db.add_user(message.from_user.id)
        await db.add_bonus(code, referal_bonus)
        await message.answer(WELCOME.format(message.from_user.full_name))
        await Permission.allowed.set()
    else:
        await message.answer(ERORR_LINK.format(message.from_user.full_name))
        await Permission.not_allowed.set()


@dp.message_handler(CommandStart())
async def start_first(message: types.Message):
    if await user_checker(message.from_user.id):
        await message.answer(HI_USER.format(message.from_user.full_name))
        await Permission.allowed.set()
    else:
        await message.answer(MESSAGE_FOR_NOT_AUTHORIZED_USERS)
        await Permission.not_allowed.set()



@dp.message_handler(CommandStart(), state=Permission.allowed)
async def start_second_registered(message: types.Message):
    await message.answer(HI_USER.format(message.from_user.full_name))


@dp.message_handler(commands=['start', 'help', 'add_product', 'invite'], state=Permission.not_allowed)
async def start_enter_code(message: types.Message):
    await message.answer(MESSAGE_FOR_NOT_AUTHORIZED_USERS)


@dp.message_handler(state=Permission.not_allowed)
async def start_second_not_registered(message: types.Message):
    try:
        code = int(message.text)
        if await user_checker(code):
            await db.add_user(message.from_user.id)
            await db.add_bonus(code, referal_bonus)
            await message.answer(WELCOME.format(message.from_user.full_name))
            await Permission.allowed.set()
        else:
            await message.answer(BAD_CODE)
    except Exception:
        await message.answer(CODE_IS_NOT_NUMBER)


@dp.callback_query_handler(text_contains="start")
async def state_reset(call: CallbackQuery):
    await call.message.delete()
    await Permission.allowed.set()
    temp = await call.message.answer(ON_STURTUP_READY)
    await asyncio.sleep(1)
    await temp.delete()