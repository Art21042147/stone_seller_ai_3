from service.catalog import manufacture, colors
from sqlalchemy import select
from db.models import Brand, Color, async_session


async def update_brands_and_colors():
    async with async_session() as session:
        async with session.begin():
            # Обновление брендов
            for title, description in manufacture:
                # Проверяем, существует ли бренд
                result = await session.execute(select(Brand).where(Brand.title == title))
                brand = result.scalars().first()

                if not brand:
                    # Если бренда нет, добавляем его
                    new_brand = Brand(title=title, description=description)
                    session.add(new_brand)

            # Обновление цветов
            for brand_title, color_name, price in colors:
                # Находим бренд по названию
                result = await session.execute(select(Brand).where(Brand.title == brand_title))
                brand = result.scalars().first()

                if brand:
                    # Проверяем, существует ли такой цвет
                    result = await session.execute(
                        select(Color).where(Color.color == color_name, Color.brand_id == brand.id)
                    )
                    color = result.scalars().first()

                    if not color:
                        # Если цвета нет, добавляем его
                        new_color = Color(color=color_name, price=price, brand_id=brand.id)
                        session.add(new_color)

        await session.commit()
