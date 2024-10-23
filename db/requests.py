from service.catalog import manufacture, colors
from sqlalchemy import select
from db.models import Brand, Color, async_session


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
