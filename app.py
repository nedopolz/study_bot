from loader import db
from utils.set_bot_commands import set_default_commands
from utils.set_users_state import on_startup_state_setter


async def on_startup(dp):
    await db.create()
    await db.create_table_products()
    await db.create_table_users()
    await db.create_table_purchase()
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await on_startup_state_setter(dp)
    await set_default_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
