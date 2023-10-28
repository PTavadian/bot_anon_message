from aiogram import types, Dispatcher
from create_bot import dp, bot

from handlers.commands import commands, bot_commands



async def start(message: types.Message):
    '''Добавление в БД при первом запуске. Добавление меню.'''
    await commands()
    await bot.send_message(message.from_user.id, 'Бот готов к работе')



async def help(message: types.Message): 
    '''Справка'''

    msg = '<b>Для работы с ботом доступны следующие команды:</b>\n'
    for i, cmd in enumerate(bot_commands):
        msg += cmd[2] + ';\n' if i != len(bot_commands) - 1 else cmd[2] + '.'
    await bot.send_message(message.from_user.id, '<i>' + msg + '</i>', parse_mode='HTML', protect_content=True, reply_markup=types.ReplyKeyboardRemove())



def regisret_handlers_other(dp : Dispatcher):
    dp.register_message_handler(start,  commands='start')
    dp.register_message_handler(help,  commands='help')


