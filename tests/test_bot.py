import pytest
from aiogram.methods import SendMessage
from aiogram.types import Message, Chat, User
from datetime import datetime

from states import StoneState


@pytest.mark.asyncio
async def test_bot_sending_message(bot):
    # create Message object
    message_result = Message(
        message_id=123,
        date=datetime.now(),
        chat=Chat(id=123, type="private"),
        from_user=User(id=456, is_bot=False, first_name="TestUser"),
        text="Test message"
    )

    bot.add_result_for(
        method=SendMessage,
        ok=True,
        result=message_result
    )

    # send message
    response = await bot.send_message(chat_id=123, text="Test message")

    # check response
    assert response.message_id == 123

    # check request
    request = bot.get_request()
    assert isinstance(request, SendMessage)
    assert request.chat_id == 123
    assert request.text == "Test message"


@pytest.mark.asyncio
async def test_fsm_transition(bot, dispatcher, fsm_context):
    await fsm_context.set_state(StoneState.length)

    state = await fsm_context.get_state()
    assert state == StoneState.length

    await fsm_context.set_state(StoneState.width)

    new_state = await fsm_context.get_state()
    assert new_state == StoneState.width
