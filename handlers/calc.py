from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states import StoneState
from keyboards import place_order_kb

calc_router = Router()


# get size stone handler
@calc_router.callback_query(F.data.startswith('confirm_'))
async def confirm_material(callback: CallbackQuery, state: FSMContext):
    # get stone data
    _, brand_title, color_data, price_rub = callback.data.split('_')

    price_rub = float(price_rub)

    await callback.answer(f'Вы выбрали материал: {brand_title}\n'
                          f'Цвет: {color_data}\n'
                          f'Цена: {price_rub:.2f} руб/м.п.\n'
                          f'Переходим к расчёту стоимости.', show_alert=True)

    # save data in FSMContext
    await state.update_data(brand_title=brand_title)
    await state.update_data(color_data=color_data)
    await state.update_data(price_rub=price_rub)

    # ask user for length
    await callback.message.answer("Пожалуйста, введите длину изделия в мм:")
    await state.set_state(StoneState.length)


# saves length and get width
async def process_length(message: Message, state: FSMContext):
    await state.update_data(length=int(message.text))
    await state.set_state(StoneState.width)
    await message.answer("Пожалуйста, введите ширину изделия в мм:")


# saves width and get cost
async def process_width(message: Message, state: FSMContext):
    await state.update_data(width=int(message.text))

    # retrieve all data from FSMContext for calculation
    data = await state.get_data()
    brand_title = data['brand_title']
    color_data = data['color_data']
    price_rub = data['price_rub']
    length = data['length']
    width = data['width']

    # calculate the total cost
    cost = (price_rub * (length / 1000) * (width / 1000)) + 5000

    # display total price with options to proceed or recalculate
    await message.answer(
        f"Стоимость изделия {brand_title} ({color_data}): {cost:.2f} руб.",
        reply_markup=place_order_kb)
    # save calculated total price to the state
    await state.update_data(cost=cost)
