from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.requests import get_brand_title, get_brand_info

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
async def brand_kb():
    brands = await get_brand_title()
    brand_builder = InlineKeyboardBuilder()
    for brand in brands:
        brand_builder.add(InlineKeyboardButton(text=brand, callback_data=f'brand_{brand}'))
    return brand_builder.adjust(2).as_markup()


# get brand info and choose color or another brand keyboard
async def brand_info_kb(brand_title):
    brand_info = await get_brand_info(brand_title)
    brand_info_builder = InlineKeyboardBuilder()
    brand_info_builder.add(InlineKeyboardButton(text="Выбор цвета",
                                                callback_data=f'color_{brand_title}'))
    brand_info_builder.add(InlineKeyboardButton(text="Выбор другого производителя",
                                                callback_data='calculator'))
    text = f"<b>{brand_title}:</b>\n{brand_info}"
    return text, brand_info_builder.adjust(1).as_markup()

# choose color keyboard
def get_color_kb(brand_title, color_data, price_rub):
    callback_data = f'confirm_{brand_title}_{color_data}_{price_rub}'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Выбрать этот цвет', callback_data=callback_data)],
        ])

# return to choose brand keyboard
brand_return_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Выбрать другого производителя', callback_data=f'calculator')],
        ])
