from aiogram import types

from data.messages_config import MESSAGE_FOR_NOT_AUTHORIZED_USERS, INLINE_NOT_FOUND_ITEM, INLINE_NOT_FOUND_ITEM_REPLY
from loader import dp, db
from states.permission import Permission
from utils.inline_search_result_maker import form_record
from utils.user_check import user_checker


@dp.inline_handler(state=Permission.not_allowed)
async def search(query: types.InlineQuery):
    print("IN not_allowed")
    await query.answer(
        results=[],
        switch_pm_text=MESSAGE_FOR_NOT_AUTHORIZED_USERS,
        switch_pm_parameter="connect_user",
        cache_time=5)


@dp.inline_handler(state=Permission.allowed)
async def search(query: types.InlineQuery):
    print(not(await user_checker(query.from_user.id)))
    if not(await user_checker(query.from_user.id)):
        print("IN if")
        await query.answer(
            results=[],
            switch_pm_text=MESSAGE_FOR_NOT_AUTHORIZED_USERS,
            switch_pm_parameter="connect_user",
            cache_time=5)
        return
    else:
        to_find = query.query
        records = await db.search_like(to_find)
        print("IN else")
        if len(records) == 0:
            await query.answer(
                results=[types.InlineQueryResultArticle(
                    id="unknown",
                    title=INLINE_NOT_FOUND_ITEM,
                    thumb_url="https://i.pinimg.com/originals/80/b0/bf/80b0bf0355822b0ad54abe93ae914f6d.jpg",
                    input_message_content=types.InputTextMessageContent(
                        message_text=INLINE_NOT_FOUND_ITEM_REPLY,
                        parse_mode="HTML"
                    ),
                ), ],
                cache_time=1)
            return

        results = []
        for i in records:
            results.append(await form_record(i))
        await query.answer(
            results
        )
        results = []
