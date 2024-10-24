from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.requests import get_brand_title, get_brand_info

# start keyboard
start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="ИНФОРМАЦИЯ ℹ️"),
     KeyboardButton(text="РАССЧЁТ 📝")],
], resize_keyboard=True)

# start calculator keyboard
calculator_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выполнить расчёт',
                          callback_data='calculator')]
])

# choose brand keyboard
async def brand_kb():
    brands = await get_brand_title()
    brand_builder = InlineKeyboardBuilder()
    for brand in brands:
        brand_builder.add(InlineKeyboardButton(text=brand, callback_data=f'brand_{brand}'))
    return brand_builder.adjust(2).as_markup()


# get brand info and choose color or another brand keyboard
async def brand_info_kb(brand_title):
    brand_info = await get_brand_info(brand_title)
    brand_info_builder = InlineKeyboardBuilder()
    brand_info_builder.add(InlineKeyboardButton(text="Выбор цвета",
                                                callback_data=f'color_{brand_title}'))
    brand_info_builder.add(InlineKeyboardButton(text="Выбор другого производителя",
                                                callback_data='calculator'))
    text = f"<b>{brand_title}:</b>\n{brand_info}"
    return text, brand_info_builder.adjust(1).as_markup()

# choose color keyboard
# color_cache = {}
#
# async def get_color_info(brand_title):
#     if brand_title in color_cache:
#         return color_cache[brand_title]
#
#     async with async_session() as session:
#         result = await session.execute(
#             select(Color).join(Brand).where(Brand.title == brand_title)
#         )
#         colors = result.scalars().all()
#     # get rate func
#     usd_to_rub_rate = get_usd_to_rub_rate()
#
#     color_info_builder = InlineKeyboardBuilder()
#     media_files = []
#     color_data = []
#
#     for color in colors:
#         image_path = f"media/{brand_title.lower()}/{color.color}.jpg"
#         media_file = FSInputFile(image_path)
#         media_files.append(media_file)
#         # convert price to RUB
#         price_in_rub = round(color.price * usd_to_rub_rate, 2)
#         price_text = f"Цена: {price_in_rub} руб/м.п."
#         # make color builder
#         color_info_builder.add(InlineKeyboardButton(text=f"Выбрать {color.color}",
#                                                     callback_data=f'select_color_{color.id}'))
#         color_info_builder.add(InlineKeyboardButton(text="Выбор другого производителя",
#                                                     callback_data='calculator'))
#         # saves color info
#         color_data.append({
#             "media_file": media_file,
#             "price_text": price_text,
#             "color_id": color.id
#         })
#
#     color_cache[brand_title] = (media_files,
#                                 color_data,
#                                 color_info_builder.adjust(1).as_markup())
#     return color_cache[brand_title]
