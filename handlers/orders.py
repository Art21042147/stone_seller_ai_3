from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from db.requests import save_order
from db.admin_requests import get_order_details
from states import OrderState
from keyboards import admin_keyboard
from config_reader import config

order_router = Router()


@order_router.callback_query(F.data == "place_order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    # save the chat ID
    await state.update_data(tg_id=callback.from_user.id)

    # requesting username
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(OrderState.name)


# save the name and request the phone number
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.phone)
    await message.answer("Введите номер телефона для связи:")


# save the phone number and request the address
async def process_phone(message: Message, state: FSMContext):
    try:
        phone = int(message.text)
        await state.update_data(phone=phone)
        await state.set_state(OrderState.address)
        await message.answer("Введите свой адрес:")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный номер телефона.")


# save the address and order details
async def process_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    # extract all data from the state
    data = await state.get_data()
    tg_id = data['tg_id']
    name = data['name']
    phone = data['phone']
    address = data['address']
    brand_title = data['brand_title']
    color_data = data['color_data']
    length = data['length']
    width = data['width']
    cost = data['cost']

    # save the order in the db and get order_id
    order_id = await save_order(
        tg_id=tg_id,
        brand_title=brand_title,
        color_data=color_data,
        length=length,
        width=width,
        cost=cost,
        name=name,
        phone=phone,
        address=address
    )

    await message.answer("Ваш заказ успешно оформлен!\n"
                         "Наши специалисты скоро свяжутся с вами.")
    # admin notification
    admin_id = int(config.admin_id.get_secret_value())
    keyboard = await admin_keyboard(order_id)

    await message.bot.send_message(
        admin_id,
        f"Поступила новая заявка от {name}.",
        reply_markup=keyboard
    )
    await state.clear()


# view order details
@order_router.callback_query(F.data.startswith('view_order_'))
async def view_order(callback: CallbackQuery):
    order_id = callback.data.split('_')[-1]
    order_details = await get_order_details(order_id)

    if order_details:
        await callback.message.answer(
            f"Заявка №{order_id}\n"
            f"Имя: {order_details['name']}\n"
            f"Телеграм ID: {order_details['tg_id']}\n"
            f"Телефон: {order_details['phone']}\n"
            f"Адрес: {order_details['address']}\n"
            f"Материал: {order_details['brand_title']}\n"
            f"Цвет: {order_details['color_data']}\n"
            f"Размеры: {order_details['length']}x{order_details['width']}\n"
            f"Сумма: {order_details['cost']:.2f} руб."
        )
    else:
        await callback.message.answer("Заказ не найден.")
    await callback.answer()
