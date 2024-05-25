from aiogram import types

from bot.models import ObjectData
from rutracker.models import FoundFile 

def get_keyboard(object_data: FoundFile):

    callback_data_mi = ObjectData(
        page_link=object_data.object_link,
        file_size=object_data.download_size,
        action='cb_more_info',
    ).pack()

    callback_data_dw = ObjectData(
        page_link=object_data.object_link,
        file_size=object_data.download_size,
        action='cb_download',
    ).pack()

    buttons = [
        [
            types.InlineKeyboardButton(text="Подробнее", callback_data=callback_data_mi),
            types.InlineKeyboardButton(text="Скачать", callback_data=callback_data_dw)
        ],
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard