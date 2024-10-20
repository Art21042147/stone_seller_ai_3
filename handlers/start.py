from aiogram.types import Message
from aiogram.types import FSInputFile

from keyboards import start_kb, calculator_kb


# greetings func
async def greetings(message: Message):
#    user_id = message.from_user.id # get telegram user ID
    user_name = message.from_user.first_name # get telegram user name
    await message.answer(
        f'<b>Добро пожаловать, {user_name}!</b>\n'
        '✨<b>Вас приветствует наш бот</b>✨',
        reply_markup=start_kb)
    logo = FSInputFile('media/appazov.jpg')
    await message.answer_photo(logo,
    'Для ознакомления с продукцией,\n'
    'нажмите кнопку\n ℹ️<b>ИНФОРМАЦИЯ</b>\n\n'
    'Чтобы рассчитать цену,\n'
    'необходимого вам изделия,\n'
    'нажмите кнопку\n 📝<b>РАССЧЁТ</b>')

# info func
async def send_group_link(message: Message):
    await message.answer("https://t.me/appazov_stone")

# start calculate func
async def calculate(message: Message):
    await message.answer(
        "<b>Обратите внимание</b>❗️\nРасчёт может не совпадать "
        "с окончательной ценой,\nесли вы ввели не корректные размеры.\n"
        "После выполнения расчёта\nвы сможете оставить заявку,\n"
        "наши специалисты свяжутся с вами,\nи после"
        " замера на месте,\nскажут Вам окончательную цену.",
        reply_markup=calculator_kb)
