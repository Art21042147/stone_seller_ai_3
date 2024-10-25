from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from states import StoneState

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
    await callback.answer()
