import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink, hcode

from data import config
from data.messages_config import ASK_FOR_AMOUNT, ASK_FOR_BONUSES_SPEND, ASK_FOR_DELIVERY_ADRESS, INVALID_AMOUNT, \
    SUCCESFUL_BONUS_SPEND, PURCHASE_SUMMARY_CAPTION, PAYMENT_BEFORE_LINK, PAYMENT_BEFORE_ID, PURCHASE_UNDO, \
    ERORR_NO_FOUND, ERORR_LESS_THEN_NEED, SUCCESFUL_PURCHASE, YOUR_MONEY_SAVE
from keyboards.inline.confirmation_bottuns import confirmation
from keyboards.inline.purchase_keyboard import paid_keyboard, start_purchase_keyboard
from loader import dp, db, bot
from states.buying import Buying
from states.permission import Permission
from utils.misc.qiwi import Payment

@dp.message_handler(Command(['start']), state=Permission.allowed, text_contains='buy')
async def start_purchase(message: Message, state: FSMContext):
    id = int((re.findall(r'^/start buy(\d{1,100})$', message.text)[0]))
    db_record = (await db.get_item_by_id(id))[0]
    id = db_record.get('id')
    price = db_record.get('price')
    url = db_record.get('url')
    description = db_record.get('description')
    name = db_record.get('name')
    file_id = db_record.get('file_id')
    chat_id = message.from_user.id
    await state.update_data(id=id, price=price, url=url, description=description, name=name, file_id=file_id)
    await bot.send_photo(chat_id=chat_id, photo=file_id,
                         caption=f'{name} по цене <b>{price}</b>\n<b>Описание:</b>\n{description}',
                         parse_mode='HTML',
                         reply_markup=start_purchase_keyboard)


@dp.callback_query_handler(state=Permission.allowed, text_contains="init")
async def take_bonuses(call: CallbackQuery, state: FSMContext):
    await Buying.amount.set()
    data = await state.get_data()
    name = data.get("name")
    await call.message.answer(ASK_FOR_AMOUNT.format(name))


@dp.message_handler(state=Buying.amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        await state.update_data(amount=amount)
        data = await state.get_data()
        price = data.get("price")
        await state.update_data(final_price=amount * price)
        bonuses = (await db.get_bonuses(message.from_user.id))[0].get('bonuses')
        if bonuses != 0:
            await message.answer(ASK_FOR_BONUSES_SPEND.format(bonuses), reply_markup=confirmation)
            await Buying.bonuses.set()
        else:
            await message.answer(ASK_FOR_DELIVERY_ADRESS)
            await Buying.address.set()
    except ValueError:
        await message.answer(INVALID_AMOUNT)


@dp.callback_query_handler(state=Buying.bonuses, text_contains="ok")
async def take_bonuses(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    temp_final_price = data.get("final_price")

    final_price = temp_final_price
    bonuses = (await db.get_bonuses(call.from_user.id))[0].get('bonuses')
    final_price -= bonuses
    if final_price <= 0:
        final_price = 1

    await state.update_data(spended_bonuses=(temp_final_price - final_price))
    await state.update_data(final_price=final_price)
    await call.message.delete()
    await call.message.answer(SUCCESFUL_BONUS_SPEND.format(final_price))
    await Buying.address.set()


@dp.callback_query_handler(state=Buying.bonuses, text_contains="not")
async def take_bonuses(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(spended_bonuses=0)
    await call.message.answer(ASK_FOR_DELIVERY_ADRESS)
    await Buying.address.set()


@dp.message_handler(state=Buying.address)
async def get_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await Buying.conformation.set()
    data = await state.get_data()
    amount = data.get("amount")
    address = data.get("address")
    name = data.get('name')
    final_price = data.get('final_price')
    file_id = data.get('file_id')
    chat_id = message.from_user.id
    await bot.send_photo(chat_id=chat_id, photo=file_id,
                         caption=PURCHASE_SUMMARY_CAPTION.format(name, amount, final_price, address),
                         parse_mode='HTML', reply_markup=confirmation)


@dp.callback_query_handler(state=Buying.conformation, text_contains="ok")
async def get_payment(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    final_price = data.get("final_price")
    payment = Payment(amount=final_price)
    payment.create()
    await state.update_data(payment=payment)

    await call.message.answer(
        "\n".join([
            PAYMENT_BEFORE_LINK.format(final_price),
            "",
            hlink(config.WALLET_QIWI, url=payment.invoice),
            PAYMENT_BEFORE_ID,
            hcode(payment.id)
        ]),
        reply_markup=paid_keyboard)

    await Buying.qiwi.set()


@dp.callback_query_handler(text="cancel", state=Buying.qiwi)
async def cancel_payment(call: types.CallbackQuery):
    await call.message.edit_text(PURCHASE_UNDO)
    await Permission.allowed.set()


@dp.callback_query_handler(text="paid", state=Buying.qiwi)
async def approve_payment(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")
    final_price = data.get("final_price")
    paid_sum = payment.check_payment()

    if paid_sum >= final_price:
        await call.message.answer(SUCCESFUL_PURCHASE)
        spended_bonuses = data.get('spended_bonuses')
        id = data.get("id")
        amonut = data.get("amount")
        adress = data.get("address")
        if (paid_sum - final_price) >= 1:
            await call.message.answer(YOUR_MONEY_SAVE.format(int(paid_sum - final_price)))
            spended_bonuses -= paid_sum-final_price
        await db.add_bonus(call.from_user.id, int(-spended_bonuses))
        await db.add_purchase_to_db(call.from_user.id, id, amonut, final_price, adress)
        await call.message.edit_reply_markup()
        await Permission.allowed.set()
    elif paid_sum < final_price:
        await call.message.answer(ERORR_LESS_THEN_NEED.format(int(final_price-paid_sum)-1), reply_markup=paid_keyboard)
        await state.update_data(final_price=(final_price-paid_sum)-1)
    else:
        await call.message.answer(ERORR_NO_FOUND)
        await Permission.allowed.set()


@dp.callback_query_handler(state=Buying.conformation, text_contains="not")
async def undo_payment(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer(PURCHASE_UNDO)
    await Permission.allowed.set()
