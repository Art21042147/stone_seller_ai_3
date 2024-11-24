import pytest_asyncio
from unittest.mock import AsyncMock, patch
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import async_db, async_session, Brand, Color
from tests.mocked_bot import MockedBot


@pytest_asyncio.fixture
def mock_message():
    message = AsyncMock()
    message.from_user.first_name = "TestUser"
    message.answer = AsyncMock()
    return message


@pytest_asyncio.fixture
def mock_callback():
    callback = AsyncMock()
    callback.message.answer = AsyncMock()
    return callback


@pytest_asyncio.fixture
async def fsm_context(storage):
    key = StorageKey(bot_id=123, chat_id=456, user_id=789)
    return FSMContext(storage=storage, key=key)


@pytest_asyncio.fixture
def mock_test_config():
    with patch("config_reader.config") as mock_config:
        mock_config.BOT_TOKEN = "test_bot_token"
        yield mock_config


@pytest_asyncio.fixture()
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


@pytest_asyncio.fixture(scope="function")
async def db_session():
    await async_db()
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def setup_test_data(db_session: AsyncSession):
    brand = Brand(title="TestBrand", description="Test Description")
    db_session.add(brand)
    await db_session.flush()

    color = Color(color="Red", price=100, brand_id=brand.id)
    db_session.add(color)
    await db_session.commit()

    return {"brand": brand, "color": color}
