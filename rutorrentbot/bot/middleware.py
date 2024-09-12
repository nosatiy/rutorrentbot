from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from bot.models import approved_users 


class GoAwayMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.approved_users = approved_users

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id not in (self.approved_users): 
            print('go away', event.from_user.username , event.from_user.id)
            await event.answer('Уходи')
            return
        print(event.from_user.username , event.from_user.id)
        return await handler(event, data)