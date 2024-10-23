from aiogram.types import CallbackQuery
from aiogram import Router, F
from keyboards import get_brand, get_brand_info


choose_router = Router()


# choose brand handler
@choose_router.callback_query(F.data == 'calculator')
async def choose_brand(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите производителя:',
                                     reply_markup=await get_brand())

# get brand info and choose color handler
@choose_router.callback_query(F.data.startswith("brand_"))
async def display_brand_info(callback: CallbackQuery):
    brand_title = callback.data.split("_")[1]  # extract brand title

    text, markup = await get_brand_info(brand_title)
    await callback.message.edit_text(text=text, reply_markup=markup)
