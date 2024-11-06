import pytest
from sqlalchemy import text

from db.models import async_db
from db.requests import *
from db.admin_requests import *
from db.models import async_session, Brand, Color


# fixture for test data
@pytest.fixture(scope="function", autouse=True)
async def setup_test_data():
    await async_db()
    async with async_session() as session:
        # add data for test
        brand = Brand(title="TestBrand", description="Test Description")
        session.add(brand)
        await session.flush()

        color = Color(color="Red", price=100, brand_id=brand.id)
        session.add(color)
        await session.commit()


# test update stone data
@pytest.mark.asyncio
async def test_update_stone_data():
    await update_brands_and_colors()


# test get stone data
@pytest.mark.asyncio
async def test_get_stone_data():
    await update_brands_and_colors()
    titles = await get_brand_title()
    assert "TestBrand" in titles

    description = await get_brand_info("TestBrand")
    assert description == "Test Description"

    color_set = await get_color("TestBrand")
    colors_list = [color.color for color in color_set]
    assert "Red" in colors_list


# test save order
@pytest.mark.asyncio
async def test_save_order():
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

    async with async_session() as session:
        result = await session.execute(
            text("SELECT * FROM orders WHERE id = :order_id"), {"order_id": order_id}
        )
        order = result.mappings().fetchone()
        assert order is not None
        assert order["name"] == "Test User"


# test get order details
@pytest.mark.asyncio
async def test_get_order():
    # create order
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


# test deleting order
@pytest.mark.asyncio
async def test_del_order():
    # create order
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
    # delete order
    is_deleted = await delete_order(order_id)
    assert is_deleted

    # make sure that the order no longer exists
    order_details = await get_order_details(order_id)
    assert order_details is None


# test for blocking and unblocking user
@pytest.mark.asyncio
async def test_ban_user():
    tg_id = 123456
    is_banned = await ban_user(tg_id)
    assert is_banned

    banned = await is_user_banned(tg_id)
    assert banned

    is_unbanned = await unban_user(tg_id)
    assert is_unbanned

    banned = await is_user_banned(tg_id)
    assert not banned
