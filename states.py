from aiogram.fsm.state import StatesGroup, State


class StoneState(StatesGroup):
    selected_material = State()
    price_rub = State()
    length = State()
    width = State()
    thickness = State()
    washing_length = State()
    washing_width = State()


class OrderState(StoneState):
    name = State()
    phone= State()
    address = State()
