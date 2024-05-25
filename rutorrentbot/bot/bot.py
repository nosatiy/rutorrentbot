import asyncio
from aiogram import Bot, Dispatcher

from rutracker.session import ru_session
from bot.commands import commands_router
from bot.callbacks import callbacks_router
from bot.middleware import GoAwayMiddleware
from settings import secret


bot = Bot(token=secret.bot_token)
dp = Dispatcher()
dp.include_router(commands_router)
dp.include_router(callbacks_router)
dp.message.middleware(GoAwayMiddleware())

async def refresh_session():
    while True:
        await asyncio.sleep(3600)
        await ru_session.reconnect()

@dp.startup()
async def on_startup():
    print('startup')
    await ru_session.login()
    asyncio.create_task(refresh_session())

@dp.shutdown()
async def on_shutdown():
    await ru_session.close_session()
    print('shutdown')
