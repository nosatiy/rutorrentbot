from aiogram import types, Router, F
from aiogram.filters.command import Command, CommandObject

from rutracker.session import ru_session
from bot.keyboards import get_keyboard

commands_router = Router()


@commands_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@commands_router.message(Command("search"))
async def cmd_search(
        message: types.Message,
        command: CommandObject,):
    args = command.args
    if not args:
        await message.answer('Напипши что искать: "/search две деффки и еще одна деффка"')

    finded_objects = await ru_session.search(args) 

    if not finded_objects:
        await message.answer('Что-то пошло пиздой или ничего не найдено, обязательно сообщи!')
        return

    for obj in finded_objects[:10]:
        idd = await message.answer(f'{obj.object_name} {obj.download_size}', reply_markup=get_keyboard(obj))


@commands_router.message(F.text)
async def go_away(message: types.Message,):
    await message.answer('Напипши что искать: "/search две деффки и еще одна деффка"')
