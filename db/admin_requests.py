from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete

from db.models import Order, BannedUser, async_session

# get order details by order_id
async def get_order_details(order_id):
    async with async_session() as session:
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.brand), selectinload(Order.color))
            .where(Order.id == order_id)
        )
        order = result.scalars().first()
        if order:
            return {
                "name": order.name,
                "tg_id": order.tg_id,
                "phone": order.phone,
                "address": order.address,
                "brand_title": order.brand.title,
                "color_data": order.color.color,
                "length": order.length,
                "width": order.width,
                "cost": order.cost
            }
        return None

# get all orders from db
async def get_all_orders():
    async with async_session() as session:
        result = await session.execute(
            select(Order)
            .options(selectinload(Order.brand), selectinload(Order.color))
        )
        orders = result.scalars().all()
        all_orders = []
        for order in orders:
            all_orders.append({
                "order_id": order.id,
                "tg_id": order.tg_id,
                "name": order.name,
                "phone": order.phone,
                "address": order.address,
                "brand_title": order.brand.title,
                "color_data": order.color.color,
                "length": order.length,
                "width": order.width,
                "cost": order.cost
            })
        return all_orders

# delete order from db
async def delete_order(order_id):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(
                delete(Order).where(Order.id == order_id)
            )
            await session.commit()
            return result.rowcount > 0


# ban user by tg_id
async def ban_user(tg_id):
    async with async_session() as session:
        existing_user = await session.execute(select(BannedUser).where(BannedUser.tg_id == tg_id))
        if existing_user.scalars().first():
            return False

        new_ban = BannedUser(tg_id=tg_id)
        session.add(new_ban)
        await session.commit()
        return True

# check if user is banned
async def is_user_banned(tg_id):
    async with async_session() as session:
        result = await session.execute(select(BannedUser).where(BannedUser.tg_id == tg_id))
        return result.scalars().first() is not None

# unban user by tg_id
async def unban_user(tg_id):
    async with async_session() as session:
        result = await session.execute(delete(BannedUser).where(BannedUser.tg_id == tg_id))
        await session.commit()
        return result.rowcount > 0
