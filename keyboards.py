from sqlalchemy import select
from db.models import Brand, async_session
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardMarkup)

# start keyboard
start_kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = "ИНФОРМАЦИЯ ℹ️"),
         KeyboardButton(text = "РАССЧЁТ 📝")],
        ], resize_keyboard=True)

# start calculator keyboard
calculator_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выполнить расчёт',
                              callback_data='calculator')]
    ])

#choose brand keyboard
async def get_brand():
    async with async_session() as session:
        result = await session.execute(select(Brand.title))
        brands = result.scalars().all()

    brand_builder = InlineKeyboardBuilder()
    for brand in brands:
        brand_builder.add(InlineKeyboardButton(text=brand, callback_data=brand))
    return brand_builder.adjust(2).as_markup()

# choose color keyboard
