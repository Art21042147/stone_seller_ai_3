from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from db.admin_requests import is_user_banned

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # check if user is banned
        if isinstance(event, (Message, CallbackQuery)):
            if await is_user_banned(event.from_user.id):
                await event.answer("Извините, вы были заблокированы и не можете пользоваться этим ботом.")
                return  # abort if the user is blocked
        return await handler(event, data)  # continue if not blocked
