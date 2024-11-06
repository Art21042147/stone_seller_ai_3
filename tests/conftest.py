import pytest
from unittest.mock import AsyncMock, patch


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
