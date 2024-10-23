from sqlalchemy import select
from db.models import Brand, Color, async_session
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, InlineKeyboardMarkup)


# start keyboard
start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ИНФОРМАЦИЯ ℹ️"),
     KeyboardButton(text="РАССЧЁТ 📝")],
], resize_keyboard=True)

# start calculator keyboard
calculator_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выполнить расчёт',
                          callback_data='calculator')]
])

# choose brand keyboard
async def get_brand():
    async with async_session() as session:
        result = await session.execute(select(Brand.title))
        brands = result.scalars().all()

    brand_builder = InlineKeyboardBuilder()
    for brand in brands:
        brand_builder.add(InlineKeyboardButton(text=brand, callback_data=f'brand_{brand}'))
    return brand_builder.adjust(2).as_markup()


# get brand info and choose color or another brand keyboard
async def get_brand_info(brand_title):
    async with async_session() as session:
        result = await session.execute(select(Brand.description).where(Brand.title == brand_title))
        brand_info = result.scalar()

    brand_info_builder = InlineKeyboardBuilder()
    brand_info_builder.add(InlineKeyboardButton(text="Выбор цвета",
                                                callback_data=f'color_{brand_title}'))
    brand_info_builder.add(InlineKeyboardButton(text="Выбор другого производителя",
                                                callback_data='calculator'))
    text = f"<b>{brand_title}:</b>\n{brand_info}"
    return text, brand_info_builder.adjust(1).as_markup()
