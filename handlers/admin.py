from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command

from config_reader import config
from keyboards import bot_manager_kb

admin_router = Router()

# admin greeting handler
@admin_router.message(Command("admin"))
async def greeting_admin(message: Message):
    admin_id = int(config.admin_id.get_secret_value())
    if message.from_user.id == admin_id:
        await message.answer(
            '➖ Если вы знаете номер заказа, нажмите кнопку\n'
            '<b>✅Посмотреть заказ</b>\n'
            'и введите номер заказа\n'
            '➖ Для просмотра всех заказов, нажмите кнопку\n'
            '📔<b>Все заказы</b>\n'
            '➖ Для удаления заказа, нажмите кнопку\n'
            '<b>❌Удалить заказ</b>\n'
            'и введите номер заказа\n'
            '➖ Чтобы заблокировать пользователя, нажмите кнопку\n'
            '<b>🔒Заблокировать пользователя</b>\n'
            'и введите ID пользователя\n'
            '➖ Чтобы разблокировать пользователя, нажмите кнопку\n'
            '<b>🔓Разблокировать пользователя</b>\n'
            'и введите ID пользователя\n',
            reply_markup=bot_manager_kb)
    else:
        await message.answer("У вас нет прав на выполнение этой команды.")
