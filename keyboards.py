from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "ИНФОРМАЦИЯ ℹ️"),
         KeyboardButton(text = "РАССЧЁТ 📝")],
        ], resize_keyboard=True
)

calculator_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Выполнить расчёт',
                              callback_data='calculator')]
    ]
)
