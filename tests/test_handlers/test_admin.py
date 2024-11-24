import pytest
from unittest.mock import AsyncMock

from aiogram.fsm.storage.base import StorageKey

from handlers.admin import *
from states import AdminState


@pytest.mark.asyncio
async def test_set_order_number(storage):
    # mock for callback
    callback = AsyncMock()
    callback.message.answer = AsyncMock()

    # create FSMContext
    state = FSMContext(
        storage=storage,
        key=StorageKey(
            bot_id=123,
            chat_id=456,
            user_id=789
        )
    )

    await set_order_number(callback=callback, state=state)

    current_state = await state.get_state()
    assert current_state == AdminState.order

    callback.message.answer.assert_called_once_with("Введите номер заказа:")
