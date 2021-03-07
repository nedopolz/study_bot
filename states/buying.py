from aiogram.dispatcher.filters.state import StatesGroup, State


class Buying(StatesGroup):
    amount = State()
    bonuses = State()
    address = State()
    conformation = State()
    qiwi = State()