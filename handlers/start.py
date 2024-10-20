from aiogram.types import Message

from keyboards import start_kb


# greetings func
async def greetings(message: Message):
    greeting_text = (
        '⭐Вас приветствует⭐\n'
        '🇦 🇵 🇵 🇦 🇿 🇴 🇻 🇸 🇹 🇴 🇳 🇪\n'
        '💎 <b>Изделия из искусственного камня</b> 💎\n\n'
        'Для ознакомления с продукцией,\n'
        'нажмите кнопку\n ℹ️<b>ИНФОРМАЦИЯ</b>\n\n'
        'Чтобы рассчитать цену,\n'
        'необходимого вам изделия,\n'
        'нажмите кнопку\n 📝<b>РАССЧЁТ</b>'
    )
    await message.answer(greeting_text,
                         reply_markup=start_kb)

# info func
async def send_group_link(message: Message):
    await message.answer("https://t.me/appazov_stone")
