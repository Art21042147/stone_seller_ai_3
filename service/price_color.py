from aiogram.types import FSInputFile

from service.usd_rate import get_usd_to_rub_rate
from db.requests import get_color

# get stone images and prices
async def get_price_color(brand_title):
    colors = await get_color(brand_title)
    result = []

    for color in colors:
        image_path = f"media/{brand_title.lower()}/{color.color}.jpg"
        media_file = FSInputFile(image_path)
        # convert price to RUB
        price_rub = round(color.price * get_usd_to_rub_rate(), 2)
        price_text = f"Цена: {price_rub} руб/м.п."
        color_data = color.color
        message_text = f"{brand_title} <b>{color_data}</b> {price_text}"
        result.append((media_file, message_text, color_data, price_rub))
    return result
