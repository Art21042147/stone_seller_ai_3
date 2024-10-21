from aiogram.types import CallbackQuery
from aiogram import Router, F

from keyboards import get_brand

choose_router = Router()

# choose brand handler
@choose_router.callback_query(F.data == 'calculator')
async def choose_brand(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Выберите производителя:',
                                  reply_markup=await get_brand())
