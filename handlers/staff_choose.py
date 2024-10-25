from aiogram.types import CallbackQuery
from aiogram import Router, F

from service.price_color import get_price_color
from keyboards import (brand_kb, brand_info_kb,
                       get_color_kb, brand_return_kb)

choose_router = Router()

# choose brand handler
@choose_router.callback_query(F.data == 'calculator')
async def choose_brand(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите производителя:',
                                     reply_markup=await brand_kb())

# get brand info and choose color handler
@choose_router.callback_query(F.data.startswith("brand_"))
async def display_brand_info(callback: CallbackQuery):
    brand_title = callback.data.split("_")[1]  # extract brand title

    text, markup = await brand_info_kb(brand_title)
    await callback.message.edit_text(text=text, reply_markup=markup)

# color selection handler
@choose_router.callback_query(F.data.startswith('color_'))
async def process_color(callback: CallbackQuery):
    brand_title = callback.data.split('_')[1]
    stone_data = await get_price_color(brand_title)
    for media_file, message_text, color_data, price_rub in stone_data:
        await callback.message.answer_photo(
            photo=media_file,
            caption=message_text,
            reply_markup=get_color_kb(brand_title, color_data, price_rub)
        )

    await callback.message.answer(
        text="Если Вам не подходят эти цвета,\n"
             "Вы можете посмотреть цвета других производителей:",
        reply_markup=brand_return_kb
    )
