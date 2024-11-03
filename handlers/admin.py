from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command

from config_reader import config
from keyboards import bot_manager_kb
from states import AdminState
from db.admin_requests import get_order_details, get_all_orders, delete_order

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

# get number for order handler
@admin_router.callback_query(F.data == 'get_order')
async def set_order_number(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите номер заказа:")
    await state.set_state(AdminState.order)

# get order handler
async def get_order_by_id(message: Message, state: FSMContext):
    try:
        order_id = int(message.text)
        order_details = await get_order_details(order_id)

        if order_details:
            await message.answer(
                f"Заявка №{order_id}\n"
                f"Имя: {order_details['name']}\n"
                f"Телеграм ID: {order_details['tg_id']}\n"
                f"Телефон: {order_details['phone']}\n"
                f"Адрес: {order_details['address']}\n"
                f"Материал: {order_details['brand_title']}\n"
                f"Цвет: {order_details['color_data']}\n"
                f"Размеры: {order_details['length']}x{order_details['width']}\n"
                f"Сумма: {order_details['cost']:.2f} руб."
            )
        else:
            await message.answer("Заказ не найден.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный номер заказа.")
    finally:
        await state.clear()

# get all orders handler
@admin_router.callback_query(F.data == "get_all_orders")
async def get_all_orders_handler(callback: CallbackQuery):
    orders = await get_all_orders()

    if not orders:
        await callback.message.answer("Заказы отсутствуют.")
    else:
        for order in orders:
            await callback.message.answer(
                f"Заявка №{order['order_id']}\n"
                f"Имя: {order['name']}\n"
                f"Телеграм ID: {order['tg_id']}\n"
                f"Телефон: {order['phone']}\n"
                f"Адрес: {order['address']}\n"
                f"Материал: {order['brand_title']}\n"
                f"Цвет: {order['color_data']}\n"
                f"Размеры: {order['length']}x{order['width']}\n"
                f"Сумма: {order['cost']:.2f} руб.\n"
                "➖➖➖➖➖➖➖➖➖➖➖"
            )
    await callback.answer()

# set order ID to delete
@admin_router.callback_query(F.data == "del_order")
async def prompt_delete_order(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите номер заказа для удаления:")
    await state.set_state(AdminState.delete_order)

# Handle order deletion by order_id
@admin_router.message(AdminState.delete_order)
async def delete_order_handler(message: Message, state: FSMContext):
    try:
        order_id = int(message.text)
        is_deleted = await delete_order(order_id)

        if is_deleted:
            await message.answer(f"Заказ №{order_id} успешно удалён.")
        else:
            await message.answer("Заказ с указанным номером не найден.")
    except ValueError:
        await message.answer("Пожалуйста, введите корректный номер заказа.")
    finally:
        await state.clear()
