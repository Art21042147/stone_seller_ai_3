import pytest
from sqlalchemy import text

from db.requests import *
from db.admin_requests import *


@pytest.mark.asyncio
async def test_update_stone_data(db_session, setup_test_data):
    await update_brands_and_colors()


@pytest.mark.asyncio
async def test_get_stone_data(setup_test_data):
    titles = await get_brand_title()
    assert "TestBrand" in titles

    description = await get_brand_info("TestBrand")
    assert description == "Test Description"

    color_set = await get_color("TestBrand")
    colors_list = [color.color for color in color_set]
    assert "Red" in colors_list


@pytest.mark.asyncio
async def test_save_order(db_session, setup_test_data):
    order_id = await save_order(
        tg_id=123,
        brand_title="TestBrand",
        color_data="Red",
        length=1000,
        width=500,
        cost=2000,
        name="Test User",
        phone=1234567890,
        address="Test Address"
    )

    async with db_session.begin():
        result = await db_session.execute(
            text("SELECT * FROM orders WHERE id = :order_id"), {"order_id": order_id}
        )
        order = result.mappings().fetchone()
        assert order is not None
        assert order["name"] == "Test User"


@pytest.mark.asyncio
async def test_get_order(db_session, setup_test_data):
    order_id = await save_order(
        tg_id=123,
        brand_title="TestBrand",
        color_data="Red",
        length=1000,
        width=500,
        cost=2000,
        name="Test User",
        phone=1234567890,
        address="Test Address"
    )
    order_details = await get_order_details(order_id)
    assert order_details["name"] == "Test User"
    assert order_details["tg_id"] == 123


@pytest.mark.asyncio
async def test_del_order(db_session, setup_test_data):
    order_id = await save_order(
        tg_id=123,
        brand_title="TestBrand",
        color_data="Red",
        length=1000,
        width=500,
        cost=2000,
        name="Test User",
        phone=1234567890,
        address="Test Address"
    )
    is_deleted = await delete_order(order_id)
    assert is_deleted

    order_details = await get_order_details(order_id)
    assert order_details is None


@pytest.mark.asyncio
async def test_ban_user(db_session):
    tg_id = 123456
    is_banned = await ban_user(tg_id)
    assert is_banned

    banned = await is_user_banned(tg_id)
    assert banned

    is_unbanned = await unban_user(tg_id)
    assert is_unbanned

    banned = await is_user_banned(tg_id)
    assert not banned
