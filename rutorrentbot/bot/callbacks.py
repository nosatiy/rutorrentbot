import shutil
from aiogram import types, F, Router
from aiogram.types import BufferedInputFile

from bot.models import ObjectData
from rutracker.session import ru_session
from torrent.ptorrent import download_file_magnet

callbacks_router = Router()

@callbacks_router.callback_query(ObjectData.filter(F.action == "cb_more_info"))
async def send_more_info(callback: types.CallbackQuery, callback_data: ObjectData):
    object_data = await ru_session.get_object_info(callback_data.page_link, target='data')
    if not object_data:
        await callback.answer('Произошел анлак', show_alert=True)
        return

    msg_text = callback.message.text
    callback.message.reply_markup.inline_keyboard[0] = callback.message.reply_markup.inline_keyboard[0][1:]

    cb_message =  '\n'.join([f'{key}{value}' for key, value in object_data.items()])
    await callback.message.edit_text(
        text=f'{msg_text}\n\n{cb_message}',
        reply_markup=callback.message.reply_markup
    )
    await callback.answer('Done', show_alert=False)


@callbacks_router.callback_query(ObjectData.filter(F.action == "cb_download"))
async def download_file(callback: types.CallbackQuery, callback_data: ObjectData):

    size_args = callback_data.file_size.strip().replace('\xa0', ' ').split(' ')

    if len(size_args) != 2 or float(size_args[0]) > 100.0 or  size_args[1].lower() != 'mb':
        await callback.answer('Что-то допизды весит, брат', show_alert=True)
        return

    internal_id = f'{callback.message.chat.id}_{callback.message.message_id}'

    magnet = await ru_session.get_object_info(callback_data.page_link, target='magnet')
    if not magnet:
        await callback.answer('Произошел анлак', show_alert=True)
        return
    
    await callback.answer('Пошла закачка, дай бог скачается!', show_alert=True)
    await callback.message.edit_text(text=callback.message.text)

    zip_file = await download_file_magnet(magnet, internal_id)
    file = BufferedInputFile.from_file(path=zip_file.file_path, filename=zip_file.file_name)
    await callback.message.answer_document(file)
    shutil.rmtree(zip_file.delete_path)