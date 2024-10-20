import asyncio
from aiogram import F
from aiogram.filters import Command

from config import bot, dp
from handlers.start import *

# start menu handlers
dp.message(F.text, Command("start"))(greetings)
dp.message(F.text == "ИНФОРМАЦИЯ ℹ️")(send_group_link)
dp.message(F.text == "РАССЧЁТ 📝")(calculate)

# start handler
@dp.message()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
