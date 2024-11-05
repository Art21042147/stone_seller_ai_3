from aiogram.fsm.state import StatesGroup, State


class StoneState(StatesGroup):
    brand_title = State()
    color_data = State()
    price_rub = State()
    length = State()
    width = State()
    cost = State()


class OrderState(StoneState):
    name = State()
    phone = State()
    address = State()


class AdminState(StatesGroup):
    order = State()
    all_orders = State()
    delete_order = State()
    ban_user = State()
    unban_user = State()
