from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete

from db.models import Order, async_session

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
