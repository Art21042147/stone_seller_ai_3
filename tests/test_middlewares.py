import pytest
from middlewares import BanCheckMiddleware


@pytest.mark.asyncio
async def test_ban_check_not_banned(mock_is_user_banned, mock_message):
    mock_is_user_banned.return_value = False

    middleware = BanCheckMiddleware()

    async def mock_handler(_, __):
        return "Handler called"

    result = await middleware(
        handler=mock_handler,
        event=mock_message,
        data={}
    )

    assert result == "Handler called"
    mock_message.answer.assert_not_called()
