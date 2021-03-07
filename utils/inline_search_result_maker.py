from aiogram.types import InlineQueryResultArticle, InputTextMessageContent

from data.messages_config import BUY_MESSAGE
from keyboards.inline.purchase_keyboard import purchase_callback_factory


async def form_record(db_record):
    id = db_record.get('id')
    name = db_record.get('name')
    description = db_record.get('description')
    price = db_record.get('price')
    url = db_record.get('url')
    to_append = InlineQueryResultArticle(
        id=id,
        title=f'{name} по цене {price}р',
        input_message_content=InputTextMessageContent(
            message_text=BUY_MESSAGE.format(name, price),
            parse_mode="HTML",
        ),
        reply_markup=await purchase_callback_factory(id, name),
        thumb_url=url,
        description=description
    )
    return to_append
