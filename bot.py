import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config_reader import config
from db.models import async_db
from db.requests import update_brands_and_colors
from handlers.staff_choose import choose_router
from handlers.start import start_router
from handlers.calc import calc_router
from handlers.calc import process_length, process_width
from handlers.orders import order_router
from handlers.orders import process_name, process_phone, process_address
from states import StoneState, OrderState


async def main():
    await async_db() # creating db
    await update_brands_and_colors() # updating brands and colors
    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(choose_router)
    dp.include_router(calc_router)
    dp.include_router(order_router)

    # registering handlers for a state
    dp.message.register(process_length, StoneState.length)
    dp.message.register(process_width, StoneState.width)
    dp.message.register(process_name, OrderState.name)
    dp.message.register(process_phone, OrderState.phone)
    dp.message.register(process_address, OrderState.address)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
