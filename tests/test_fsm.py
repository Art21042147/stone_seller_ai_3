import pytest
from aiogram.fsm.context import FSMContext
from unittest.mock import AsyncMock

from handlers.orders import process_address


@pytest.fixture
def mock_state():
    return AsyncMock(spec=FSMContext)


async def test_order_processing_handler(mock_state):
    message = AsyncMock()
    message.text = "1000"
    await process_address(message, mock_state)

    mock_state.update_data.assert_called_once_with(length=1000)
    message.answer.assert_called_once_with("Теперь введите ширину изделия в мм:")
