from aiogram import types, Dispatcher 
from create_bot import dp, bot
from data_base import db
from handlers import message_answer as msg_answ
from keyboards import message_kb, kb_message_2

from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup 


class FSMDel(StatesGroup):
    get_name = State()
    check_name = State()




async def help(message : types.Message, state: FSMContext):
    '''Команда help'''
    if message.chat.type == 'private': 

        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_10_helh', language)

        await message.reply(msg, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()




async def del_group_name(message : types.Message):
    '''Возвращает список с группами пользователя'''
    if message.chat.type == 'private':
        await FSMDel.get_name.set()
        lst = db.get_list_group(message.from_user.id)
        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_12_which_remote', language)
        hid_msg = msg_answer.get_msg('reply_13_choose', language)
        await message.reply(msg, reply_markup=message_kb.get_kb_list_group(lst, hid_msg)) 




async def get_group_name(message : types.Message, state: FSMContext):
    '''Принимает название удаляемой группы'''
    if message.text == '/cancel':
        await state.finish()
        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_6_ok', language)
        await message.reply(msg, reply_markup=types.ReplyKeyboardRemove()) 

    else:
        async with state.proxy() as dict_state:
            dict_state['get_name'] =  message.text
        await FSMDel.next()

        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_11_delete', language)
        await message.reply(msg, reply_markup=kb_message_2)




async def check_group_name(message : types.Message, state: FSMContext):
     '''Удаляет название группы из списка пользователя'''
     async with state.proxy() as dict_state:
        db.del_name_group(message.from_user.id, dict_state['get_name']) 
        await state.finish()
        msg_answer = msg_answ.Text()
        language = message.__dict__['_values']['from']['language_code']
        msg = msg_answer.get_msg('reply_9_ready', language)
        await message.reply(msg, reply_markup=types.ReplyKeyboardRemove())





def regisret_handlers_other(dp : Dispatcher):
    dp.register_message_handler(help, commands=['help', 'start'], state='*') 
    dp.register_message_handler(del_group_name, commands='delete', state=None) 
    dp.register_message_handler(get_group_name, state=FSMDel.get_name) 
    dp.register_message_handler(check_group_name, commands='delete', state=FSMDel.check_name) 





