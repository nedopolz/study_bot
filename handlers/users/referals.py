from aiogram import types

from data.messages_config import REFERALS_LINK, YOUR_BONUSES
from loader import dp, bot, db
from states.permission import Permission


@dp.message_handler(commands="invite", state=Permission.allowed)
async def start(message: types.Message):
    user_id = str(message.from_user.id)
    bot_name = (await bot.me).username
    await message.answer(REFERALS_LINK.format(bot_name, user_id))


@dp.message_handler(commands="bonuses", state=Permission.allowed)
async def start(message: types.Message):
    id = message.from_user.id
    amount = (await db.get_bonuses(id))[0].get('bonuses')
    await message.answer(YOUR_BONUSES.format(amount))
