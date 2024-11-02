from service.catalog import manufacture, colors
from sqlalchemy import select
from db.models import Brand, Color, Order, async_session

# update data from catalog
async def update_brands_and_colors():
    async with async_session() as session:
        async with session.begin():
            for title, description in manufacture:
                result = await session.execute(select(Brand).where(Brand.title == title))
                brand = result.scalars().first()

                if not brand:
                    new_brand = Brand(title=title, description=description)
                    session.add(new_brand)

            for brand_title, color_name, price in colors:
                result = await session.execute(select(Brand).where(Brand.title == brand_title))
                brand = result.scalars().first()

                if brand:
                    result = await session.execute(
                        select(Color).where(Color.color == color_name,
                                            Color.brand_id == brand.id)
                    )
                    color = result.scalars().first()

                    if not color:
                        new_color = Color(color=color_name, price=price, brand_id=brand.id)
                        session.add(new_color)

        await session.commit()


# get brand title from db
async def get_brand_title():
    async with async_session() as session:
        return await session.scalars(select(Brand.title))

# get brand info from db
async def get_brand_info(brand_title):
    async with async_session() as session:
        return await session.scalar(select(Brand.description).where(Brand.title == brand_title))

# get color from db
async def get_color(brand_title):
    async with async_session() as session:
        return await session.scalars(
            select(Color).join(Brand).where(Brand.title == brand_title))

# save order with user data in db
async def save_order(tg_id, brand_title, color_data, length, width, cost, name, phone, address):
    async with async_session() as session:
        # get brand_id and color_id
        result = await session.execute(select(Brand).where(Brand.title == brand_title))
        brand = result.scalars().first()

        result = await session.execute(select(Color).where(
            Color.color == color_data, Color.brand_id == brand.id))
        color = result.scalars().first()

        # create a new order with user data
        new_order = Order(
            tg_id=tg_id,
            name=name,
            phone=phone,
            address=address,
            length=length,
            width=width,
            cost=cost,
            brand_id=brand.id,
            color_id=color.id
        )

        session.add(new_order)
        await session.commit()
