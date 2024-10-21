import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config_reader import config
from handlers.staff_choose import choose_router
from handlers.start import start_router


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(choose_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot,
                           allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
