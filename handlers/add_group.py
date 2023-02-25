from aiogram import types, Dispatcher 
from create_bot import dp, bot
from data_base import db
import asyncio
from handlers import message_answer as msg_answ





async def add_group(message: types.Message):

    msg_answer = msg_answ.Text()
    language = message.__dict__['_values']['from']['language_code']

    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        db.append_group(message.chat.id, message.chat.title)
        msg = msg_answer.get_msg('reply_7_acrivated', language)
        await message.reply(msg)
        await asyncio.sleep(4)
        await bot.delete_message(message.chat.id, message.message_id) 
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id+1) 

    elif message.chat.type == 'private':
        msg = msg_answer.get_msg('reply_8_make_admin', language)
        await message.reply(msg)
        await asyncio.sleep(4)
        await bot.delete_message(message.chat.id, message.message_id) 
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id+1)





def regisret_handlers_group(dp : Dispatcher):
    dp.register_message_handler(add_group, commands='add') 

















