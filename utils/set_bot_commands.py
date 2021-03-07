from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Помощь"),
        types.BotCommand("invite", "Пригласить реферала"),
        types.BotCommand("bonuses", "Узнать количество бонусов"),
        types.BotCommand("add_product", "Добавить продукт")
    ])
