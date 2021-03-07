import logging

from aiogram import Dispatcher

from data.config import admins
from data.messages_config import ADMIN_NOTIFY


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, ADMIN_NOTIFY)
        except Exception as err:
            logging.exception(err)
