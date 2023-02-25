from aiogram import types, Dispatcher 
from create_bot import dp, bot
from data_base import db
from handlers import message_answer as msg_answ
from keyboards import message_kb, kb_message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup 
from aiogram.dispatcher.filters import Text 
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaDocument, InputMediaAudio


class FSMMess(StatesGroup):    
    group_name = State()
    id_msg = State()
    msg_text = State()
    file_id = State()
    photo_id = State()
    viveo_id = State()
    voice_id = State()
    trash = State() #исключает дублирование сообщений при ебучей итерации функции
    poll = State()
    document_id = State() 
    audio_id = State() 
    lst_group = State()
 



async def check_files(message: types.Message, state: FSMContext):
    '''Пересылает сообщение обратно в чат с ботом для проверки'''
    if message.chat.type == 'private':
        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']

        async with state.proxy() as dict_state: 
            if not dict_state._data:
                msg = msg_answer.get_msg('reply_1_send_nothing', language)
                await message.reply(msg)
                await state.finish()

            else:
                media = []

                if dict_state._data.get('poll') or dict_state._data.get('voice_id'):
                    await bot.copy_message(message.from_user.id, message.chat.id, dict_state['trash'])


                elif dict_state._data.get('photo_id') or dict_state._data.get('viveo_id'):
                    
                    if dict_state._data.get('photo_id'):
                        for photo_id in dict_state['photo_id']:
                            media.append(InputMediaPhoto(photo_id))

                    if dict_state._data.get('viveo_id'):
                        for video_id in dict_state['viveo_id']:
                            media.append(InputMediaVideo(video_id))

                    await bot.send_media_group(message.from_user.id, media)
                    

                elif dict_state._data.get('audio_id'):
                    for audio_id in dict_state['audio_id']:
                        media.append(InputMediaAudio(audio_id))
                    await bot.send_media_group(message.from_user.id, media)


                elif dict_state._data.get('document_id'):
                    for document_id in dict_state['document_id']:
                        media.append(InputMediaDocument(document_id))
                    await bot.send_media_group(message.from_user.id, media)


                else:
                    await bot.send_message(message.from_user.id, dict_state['msg_text'])


                await FSMMess.next()

                lst = db.get_list_group(message.from_user.id)
                dict_state['lst_group'] = lst
                msg = msg_answer.get_msg('reply_2_where_to_send', language)
                hid_msg = msg_answer.get_msg('reply_13_choose', language)
                if lst:
                    await message.reply(msg, reply_markup=message_kb.get_kb_list_group(lst, hid_msg))
                else:
                    await message.reply(msg, reply_markup=kb_message)




async def cancel_handler(message: types.Message, state: FSMContext):
    '''Выход из состояний'''
    if message.chat.type == 'private':
        current_state = await state.get_state() #проверяем в каком состоянии сейчас находится бот
        if current_state is None:
            return
        await state.finish() 
        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_6_ok', language)
        await message.reply(msg, reply_markup=types.ReplyKeyboardRemove()) 




async def get_files(message : types.Message, state: FSMContext):
    '''Сохраняет id полученных файлов'''
    if message.chat.type == 'private': 

        if message.caption:
            msg = message.caption
        elif message.text:
            msg = message.text
        else:
            msg = None


        async with state.proxy() as dict_state:
            dict_state['id_msg'] = message.message_id

            if message.photo:
                if dict_state._data.get('photo_id'):
                    index_id_photo = dict_state['photo_id']
                    index_id_photo.append(message.photo[-1].file_id)
                else:    
                    index_id_photo = list()
                    index_id_photo.append(message.photo[-1].file_id)
                dict_state['photo_id'] = index_id_photo

            if message.video:
                if dict_state._data.get('viveo_id'):
                    index_id_video = dict_state['viveo_id']
                    index_id_video.append(message.video.file_id)
                else:    
                    index_id_video = list()
                    index_id_video.append(message.video.file_id)
                dict_state['viveo_id'] = index_id_video

            if message.document:
                if dict_state._data.get('document_id'):
                    index_id_document = dict_state['document_id']
                    index_id_document.append(message.document.file_id)
                else:    
                    index_id_document = list()
                    index_id_document.append(message.document.file_id)
                dict_state['document_id'] = index_id_document                

            if message.audio:
                if dict_state._data.get('audio_id'):
                    index_id_audio = dict_state['audio_id']
                    index_id_audio.append(message.audio.file_id)
                else:    
                    index_id_audio = list()
                    index_id_audio.append(message.audio.file_id)
                dict_state['audio_id'] = index_id_audio                

            if message.voice:
                dict_state['voice_id'] = message.voice.file_id

            if msg:
                dict_state['msg_text'] = msg

            dict_state['media_group_id'] = message.media_group_id

            if not dict_state._data.get('trash'): #исключает дублирование сообщений при ебучей итерации функции
                dict_state['trash'] = message.message_id

            if message.poll: 
                dict_state['poll'] = message.message_id

        if message.message_id == dict_state['trash']:
                                
            msg_answer = msg_answ.Text()
            language = message.__dict__['_values']['from']['language_code']
            msg = msg_answer.get_msg('reply_3_anything_else', language)
            hid_msg = msg_answer.get_msg('reply_14_type_file', language)
            kb = message_kb.get_kb(hid_msg) 
            await bot.send_message(message.from_id, msg, reply_markup=kb)




async def send_files(message: types.Message, state: FSMContext):  
    '''Пересылает сообщение в группу'''
    if message.chat.type == 'private':
        async with state.proxy() as dict_state:
            dict_state['group_name'] = message.text

        chat_id = db.get_id_group(message.text)

        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']

        try:
            chat_users = await bot.get_chat_member(chat_id=chat_id[0], user_id=message.from_user.id)

            if chat_users.can_post_messages:
                media = []

                if dict_state._data.get('poll') or dict_state._data.get('voice_id'):
                    await bot.copy_message(*chat_id, message.chat.id, dict_state['trash'])


                elif dict_state._data.get('photo_id') or dict_state._data.get('viveo_id'):
                    
                    if dict_state._data.get('photo_id'):
                        for photo_id in dict_state['photo_id']:
                            media.append(InputMediaPhoto(photo_id))

                    if dict_state._data.get('viveo_id'):
                        for video_id in dict_state['viveo_id']:
                            media.append(InputMediaVideo(video_id))

                    await bot.send_media_group(*chat_id, media)


                elif dict_state._data.get('audio_id'):
                    for audio_id in dict_state['audio_id']:
                        media.append(InputMediaAudio(audio_id))
                    await bot.send_media_group(*chat_id, media)


                elif dict_state._data.get('document_id'):
                    for document_id in dict_state['document_id']:
                        media.append(InputMediaDocument(document_id))
                    await bot.send_media_group(message.from_user.id, media)


                else:
                    await bot.send_message(*chat_id, dict_state['msg_text'])

                msg = msg_answer.get_msg('reply_9_ready', language)
                await message.reply(msg, reply_markup=types.ReplyKeyboardRemove())

                if dict_state['lst_group']:
                    if not message.text in dict_state['lst_group']:
                        db.append_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)
                else:
                    db.append_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.text)


            else:
                msg = msg_answer.get_msg('reply_5_send_error', language)
                await bot.send_message(message.chat.id, msg, reply_markup=types.ReplyKeyboardRemove())


        except:

            msg = msg_answer.get_msg('reply_4_no_group', language)
            await bot.send_message(message.from_user.id, msg, reply_markup=types.ReplyKeyboardRemove())

        await state.finish() 




def regisret_handlers_message(dp : Dispatcher):

    dp.register_message_handler(check_files, commands='check') 
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(get_files,)
    dp.register_message_handler(get_files, content_types=['photo', 'video', 'audio', 'poll', 'voice', 'document'])
    dp.register_message_handler(send_files, state=FSMMess.group_name) 



