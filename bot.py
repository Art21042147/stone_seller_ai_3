import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_reader import config
from handlers.start import start_router


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
