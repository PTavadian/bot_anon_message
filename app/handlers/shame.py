from aiogram import types, Dispatcher 
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio

from database.workGroup import get_group
from database.workUser import add_user_group, get_user_groups
from database.cache import redis_client
from handlers.spam import delete_messages

from keyboards.message_kb import check_kb, get_kb_list_group



class FSMShame(StatesGroup):
    check = State()
    send = State()



async def catch_files(message: types.Message, state: FSMContext): 
    if message.chat.type == 'private': 

        if message.caption:
            msg = message.caption
        elif message.text:
            msg = message.text
        else:
            msg = None


        async with state.proxy() as data:
            data['id_msg'] = message.message_id
            data['msg'] = msg

            if message.photo:
                if data._data.get('photo_id'):
                    index_id_photo = data['photo_id']
                    index_id_photo.append(message.photo[-1].file_id)
                else:    
                    index_id_photo = list()
                    index_id_photo.append(message.photo[-1].file_id)
                data['photo_id'] = index_id_photo

            if message.video:
                if data._data.get('viveo_id'):
                    index_id_video = data['viveo_id']
                    index_id_video.append(message.video.file_id)
                else:    
                    index_id_video = list()
                    index_id_video.append(message.video.file_id)
                data['viveo_id'] = index_id_video

            if message.document:
                if data._data.get('document_id'):
                    index_id_document = data['document_id']
                    index_id_document.append(message.document.file_id)
                else:    
                    index_id_document = list()
                    index_id_document.append(message.document.file_id)
                data['document_id'] = index_id_document                

            if message.audio:
                if data._data.get('audio_id'):
                    index_id_audio = data['audio_id']
                    index_id_audio.append(message.audio.file_id)
                else:    
                    index_id_audio = list()
                    index_id_audio.append(message.audio.file_id)
                data['audio_id'] = index_id_audio                

            if message.voice:
                data['voice_id'] = message.voice.file_id

            if msg:
                data['msg_text'] = msg

            data['media_group_id'] = message.media_group_id

            if message.poll: 
                data['poll'] = message.message_id

        await FSMShame.check.set()

    await bot.send_message(message.from_user.id, 'Можно оправлять несколько файлов', reply_markup=check_kb())




async def check_files(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':

        async with state.proxy() as data:
            if not data._data:

                await message.reply('нету данных')
                await state.finish()

            else:
                media = []

                if data._data.get('poll') or data._data.get('voice_id'):
                    await bot.copy_message(message.from_user.id, message.chat.id, data['id_msg'])


                elif data._data.get('photo_id') or data._data.get('viveo_id'):
                    
                    if data._data.get('photo_id'):
                        for photo_id in data['photo_id']:
                            media.append(InputMediaPhoto(photo_id))

                    if data._data.get('viveo_id'):
                        for video_id in data['viveo_id']:
                            media.append(InputMediaVideo(video_id))

                    await bot.send_media_group(message.from_user.id, media)

                elif data._data.get('audio_id'):
                    for audio_id in data['audio_id']:
                        media.append(InputMediaAudio(audio_id))
                    await bot.send_media_group(message.from_user.id, media)


                elif data._data.get('document_id'):
                    for document_id in data['document_id']:
                        media.append(InputMediaDocument(document_id))
                    await bot.send_media_group(message.from_user.id, media)

                else:
                    await bot.send_message(message.from_user.id, data['msg_text'])

                await FSMShame.send.set()

                groups = get_user_groups(message.from_user.id) 
                data['groups'] = groups

                if groups:
                    await bot.send_message(message.from_user.id, 'выбери название группы или напиши новое', reply_markup=get_kb_list_group(groups))
                else:
                    await bot.send_message(message.from_user.id, 'напиши название группы', reply_markup=check_kb())




async def send_shame(message: types.Message, state: FSMContext):  
    if message.chat.type == 'private':
        async with state.proxy() as data:
            chat_id = get_group(title=message.text)  

        try:
            chat_users = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)

            if chat_users.can_post_messages:
                media = []

                if data._data.get('poll') or data._data.get('voice_id'):
                    await bot.copy_message(chat_id, message.chat.id, data['id_msg'])

                elif data._data.get('photo_id') or data._data.get('viveo_id'):
                    
                    if data._data.get('photo_id'):
                        for photo_id in data['photo_id']:
                            media.append(InputMediaPhoto(photo_id))

                    if data._data.get('viveo_id'):
                        for video_id in data['viveo_id']:
                            media.append(InputMediaVideo(video_id))

                    await bot.send_media_group(chat_id, media)

                elif data._data.get('audio_id'):
                    for audio_id in data['audio_id']:
                        media.append(InputMediaAudio(audio_id))
                    await bot.send_media_group(chat_id, media)

                elif data._data.get('document_id'):
                    for document_id in data['document_id']:
                        media.append(InputMediaDocument(document_id))
                    await bot.send_media_group(message.from_user.id, media)

                else:
                    await bot.send_message(chat_id, data['msg_text'])

                await message.reply('Готово', reply_markup=types.ReplyKeyboardRemove())

                if not message.text in data['groups']:
                    add_user_group(message.from_user.id, chat_id, message.text)
     
            else:
                await bot.send_message(message.chat.id, 'Ошибка отправления. Проверьте права бота.', reply_markup=types.ReplyKeyboardRemove())

        except:
            await bot.send_message(message.from_user.id, 'Эта группа не использует бота. Нажмите: /Help', reply_markup=types.ReplyKeyboardRemove())

        await state.finish() 




def regisret_handlers_shame(dp : Dispatcher):
    dp.register_message_handler(catch_files, content_types=['text', 'photo', 'video', 'audio', 'poll', 'voice', 'document'])
    dp.register_message_handler(check_files, state=FSMShame.check) 
    dp.register_message_handler(send_shame, state=FSMShame.send) 




