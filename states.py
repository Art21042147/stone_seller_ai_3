from aiogram.fsm.state import StatesGroup, State


class StoneState(StatesGroup):
    brand_title = State()
    color_data = State()
    price_rub = State()
    length = State()
    width = State()


class OrderState(StoneState):
    name = State()
    phone= State()
    address = State()
