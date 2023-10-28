from aiogram import types, Dispatcher 
from create_bot import dp, bot
from database.workGroup import add_group as add_gr
import asyncio



async def add_group(message: types.Message):
    if message.chat.type == 'supergroup' or message.chat.type == 'group':
        add_gr(message.chat.id, message.chat.title, True)

        await message.reply('Бот активирован')
        await asyncio.sleep(4)
        await bot.delete_message(message.chat.id, message.message_id) 
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id+1) 

    elif message.chat.type == 'private':
        await message.reply('Сделай бота администратором группы, затем активируй командой: /add')
        await asyncio.sleep(4)
        await bot.delete_message(message.chat.id, message.message_id) 
        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, message.message_id+1)



def regisret_handlers_group(dp : Dispatcher):
    dp.register_message_handler(add_group, commands='add') 



