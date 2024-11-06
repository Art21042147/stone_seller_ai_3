from unittest.mock import AsyncMock, patch
import pytest

@pytest.fixture
def mock_bot():
    with patch("aiogram.Bot") as MockBot:
        mock_bot_instance = MockBot.return_value
        mock_bot_instance.send_message = AsyncMock()
        yield mock_bot_instance

@pytest.fixture
def mock_dispatcher(mock_bot):
    with patch("aiogram.Dispatcher") as MockDispatcher:
        dp = MockDispatcher.return_value
        dp.register_message_handler = AsyncMock()
        dp.register_callback_query_handler = AsyncMock()
        yield dp

@pytest.mark.asyncio
async def test_router_registration(mock_dispatcher):
    mock_dispatcher.register_message_handler.assert_called()
    mock_dispatcher.register_callback_query_handler.assert_called()
