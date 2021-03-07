import os
import logging

import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.config import admins
from data.messages_config import ASK_FOR_PRODUCT_NAME, YOU_CANT_USE_THIS_COMMAND, ASK_FOR_PRODUCT_DESCRIPTION, \
    ASK_FOR_PRODUCT_PRICE, ASK_FOR_PRODUCT_PHOTO, INCORRECT_PRICE, PRODUCT_SUMMARY_CAPTION, PRODUCT_CONFORMATION, \
    PRODUCT_UNDO, PRODUCT_WRITTEN_IN_DB, UNKNOWN_ERORR
from keyboards.inline.confirmation_bottuns import confirmation
from loader import dp, bot, db, ImLoad
from states.admin_product_addition import AddProduct

from states.permission import Permission


@dp.message_handler(Command("add_product"), state=Permission.allowed)
async def start_product_addition(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(ASK_FOR_PRODUCT_NAME)
        await AddProduct.name.set()
    else:
        await message.answer(YOU_CANT_USE_THIS_COMMAND)


@dp.message_handler(state=AddProduct.name)
async def get_product_description(message: types.Message, state: FSMContext):
    product_name = message.text
    await message.answer(ASK_FOR_PRODUCT_DESCRIPTION.format(product_name))
    await state.update_data(name=product_name)
    await AddProduct.description.set()


@dp.message_handler(state=AddProduct.description)
async def get_product_price(message: types.Message, state: FSMContext):
    description = message.text
    await message.answer(ASK_FOR_PRODUCT_PRICE)
    await state.update_data(description=description)
    await AddProduct.price.set()


@dp.message_handler(state=AddProduct.price)
async def get_product_photo(message: types.Message, state: FSMContext):
    price = message.text
    try:
        price = int(price)
        await state.update_data(price=price)
        await message.answer(ASK_FOR_PRODUCT_PHOTO)
        await AddProduct.photo.set()
    except ValueError as e:
        logging.exception(e)
        await message.answer(INCORRECT_PRICE)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=AddProduct.photo)
async def summary(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(file_id=file_id)
    await message.photo[-1].download(
        fr'.\photos\{file_id}.jpg')  # TODO DANGER path

    data = await state.get_data()
    photo = data.get("file_id")
    try:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo,
                             caption=PRODUCT_SUMMARY_CAPTION.format(data.get("name"), data.get("description"),
                                                                    data.get("price")))
        await message.answer(PRODUCT_CONFORMATION, reply_markup=confirmation)
    except Exception as e:
        logging.exception(e)
        await message.answer(UNKNOWN_ERORR)
        await Permission.allowed.set()


@dp.callback_query_handler(state=AddProduct.photo, text_contains="not")
async def undo_product_addition(call: CallbackQuery, state: FSMContext):
    await call.message.answer(PRODUCT_UNDO)
    data = await state.get_data()
    file_id = data.get("file_id")
    os.remove(
        fr'.\photos\{file_id}.jpg')  # TODO DANGER path
    await Permission.allowed.set()


@dp.callback_query_handler(state=AddProduct.photo, text_contains="ok")
async def confirm_product_addition(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    file_id = data.get("file_id")
    url = ImLoad.upload_photo(file_id)
    await state.update_data(url=url)
    await state.finish()
    await Permission.allowed.set()
    name = data.get("name")
    description = data.get("description")
    file_id = data.get("file_id")
    price = int(data.get("price"))
    await db.add_product_to_db(file_id, url, name, description, price)
    await call.message.answer(PRODUCT_WRITTEN_IN_DB, reply_markup=None)
