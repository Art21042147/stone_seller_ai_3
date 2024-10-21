from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

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
brands = ['Corian', 'Tristone', 'Grandex', 'Montelli']

async def get_brand():
    brand_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=brand, callback_data=brand)] for brand in brands
    ])
    return brand_kb

