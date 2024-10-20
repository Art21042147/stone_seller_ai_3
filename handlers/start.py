from aiogram.types import Message
from aiogram.types import FSInputFile

from keyboards import start_kb


# greetings func
async def greetings(message: Message):
#    user_id = message.from_user.id # get telegram user ID
    user_name = message.from_user.username # get telegram user name
    await message.answer(
        f'<b>Добро пожаловать, {user_name}!</b>\n'
        '✨<b>Вас приветствует наш бот</b>✨',
        reply_markup=start_kb)
    logo = FSInputFile('media/appazov.jpg')
    await message.answer_photo(logo,
    'Для ознакомления с продукцией,\n'
    'нажмите кнопку\n ℹ️<b>ИНФОРМАЦИЯ</b>\n\n'
    'Чтобы рассчитать цену,'
    'необходимого вам изделия,\n'
    'нажмите кнопку\n 📝<b>РАССЧЁТ</b>')

# info func
async def send_group_link(message: Message):
    await message.answer("https://t.me/appazov_stone")
