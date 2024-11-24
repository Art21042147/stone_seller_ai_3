import pytest

from handlers.start import *


@pytest.mark.asyncio
async def test_send_group_link(mock_message):
    await send_group_link(mock_message)

    mock_message.answer.assert_any_call("https://t.me/appazov_stone")


@pytest.mark.asyncio
async def test_calculate(mock_message):
    await calculate(mock_message)

    expected_text = (
        "<b>Обратите внимание</b>❗️\nРасчёт является предварительным.\n"
        "Стоимость будет зависеть от материала изготовления,\n"
        "сложности работы, типа обработки и других параметров.\n"
        "После выполнения предварительного расчёта\nвы сможете оставить заявку,\n"
        "наши специалисты свяжутся с вами,\n"
        "и после замеров на месте,\nопределят окончательную цену."
    )

    mock_message.answer.assert_any_call(expected_text, reply_markup=calculator_kb)


@pytest.mark.asyncio
async def test_all_messages(mock_message):
    await all_messages(mock_message)

    mock_message.answer.assert_any_call("Введите команду /start, чтобы начать общение.")
