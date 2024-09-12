from pydantic import BaseModel
from aiogram.filters.callback_data import CallbackData


class ObjectData(CallbackData, prefix="obj_data"):
    page_link: str
    file_size: str
    action: str


approved_users = {507541585, 148554314, 31739163, 317391635}