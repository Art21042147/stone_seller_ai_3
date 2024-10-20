from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

from keyboards import start_kb, calculator_kb


start_router = Router()

# greetings handler
@start_router.message(F.text, Command("start"))
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

# info handler
@start_router.message(F.text == "ИНФОРМАЦИЯ ℹ️")
async def send_group_link(message: Message):
    await message.answer("https://t.me/appazov_stone")

# start calculate handler
@start_router.message(F.text == "РАССЧЁТ 📝")
async def calculate(message: Message):
    await message.answer(
        "<b>Обратите внимание</b>❗️\nРасчёт может не совпадать "
        "с окончательной ценой,\nесли вы ввели не корректные размеры.\n"
        "После выполнения расчёта\nвы сможете оставить заявку,\n"
        "наши специалисты свяжутся с вами,\nи после"
        " замера на месте,\nскажут Вам окончательную цену.",
        reply_markup=calculator_kb)


# start handler
@start_router.message()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')
