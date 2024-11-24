import pytest_asyncio
from unittest.mock import AsyncMock, patch
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, User, Chat

from db.models import async_db, async_session, Brand, Color
from tests.mocked_bot import MockedBot


@pytest_asyncio.fixture
def mock_message():
    message = AsyncMock(spec=Message)
    message.from_user = User(id=456, is_bot=False, first_name="TestUser")
    message.chat = Chat(id=123, type="private")
    message.text = "Hello"
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


@pytest_asyncio.fixture
async def storage():
    temp_storage = MemoryStorage()
    try:
        yield temp_storage
    finally:
        await temp_storage.close()


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


@pytest_asyncio.fixture
def mock_is_user_banned():
    with patch("db.admin_requests.is_user_banned", new_callable=AsyncMock) as mock:
        yield mock
