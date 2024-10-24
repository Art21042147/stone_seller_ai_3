from aiogram.types import CallbackQuery
from aiogram import Router, F
from keyboards import brand_kb, brand_info_kb

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


# @choose_router.callback_query(F.data.startswith('color_'))
# async def process_color(callback: CallbackQuery):
#     brand_title = callback.data.split('_')[1]
#
#     media_files, color_data, color_kb = await get_color_info(brand_title)
#
#     # Отправляем изображения и цены
#     for idx, media_file in enumerate(media_files):
#         await callback.message.answer_photo(photo=media_file, caption=color_data[idx]["price_text"])
#
#     # Отправляем клавиатуру для выбора цвета
#     await callback.message.answer("Выберите цвет:", reply_markup=color_kb)
