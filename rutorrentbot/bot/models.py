from pydantic import BaseModel
from aiogram.filters.callback_data import CallbackData


class ObjectData(CallbackData, prefix="obj_data"):
    page_link: str
    file_size: str
    action: str

