import pytest
from handlers.admin import *
from states import AdminState


@pytest.mark.asyncio
async def test_set_order_number(mock_callback, fsm_context):
    await set_order_number(callback=mock_callback, state=fsm_context)

    current_state = await fsm_context.get_state()
    assert current_state == AdminState.order

    mock_callback.message.answer.assert_called_once_with("Введите номер заказа:")
