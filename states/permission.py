from aiogram.dispatcher.filters.state import StatesGroup, State


class Permission(StatesGroup):
    allowed = State()
    not_allowed = State()