import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tests.mocked_bot import MockedBot


@pytest.fixture
def mock_test_config():
    with patch("config_reader.config") as mock_config:
        mock_config.BOT_TOKEN = "test_bot_token"
        yield mock_config


@pytest_asyncio.fixture
def mock_message():
    message = AsyncMock()
    message.from_user.first_name = "TestUser"
    message.answer = AsyncMock()
    return message


@pytest.fixture()
def bot():
    return MockedBot()


@pytest_asyncio.fixture
async def dispatcher():
    dp = Dispatcher()
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture
async def storage():
    temp_storage = MemoryStorage()
    try:
        yield temp_storage
    finally:
        await temp_storage.close()


@pytest_asyncio.fixture
def mock_session():
    with patch("db.models.async_session", new_callable=AsyncMock) as mock_session:
        yield mock_session
