from aiogram.types import BotCommand
from create_bot import dp, bot



bot_commands = (

    ('start', 'Начало работы с ботом', '/start - активирует бота'),
    ('help', 'Помощь и справка', '/help - дает справочную информацию'),
    ('cancel', 'Отменить', '/cancel - отменяет любое действие'),
#    ('add', '', '/add - активация бота'),
#    ('', '', ''),
#    ('', '', ''),
#    ('', '', ''),
)



async def commands():
    '''Добавление команд'''

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)



