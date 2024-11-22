import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_message():
    message = AsyncMock()
    message.from_user.first_name = "TestUser"
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_bot():
    return AsyncMock()


@pytest.fixture
def mock_session():
    with patch("db.models.async_session", new_callable=AsyncMock) as mock_session:
        yield mock_session


@pytest.fixture
def mock_state():
    return AsyncMock()
