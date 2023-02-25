from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 
from data_base import db


from create_bot import dp


async def on_startup(_):
    db.sql_start()


from handlers import add_group, other, add_message


add_group.regisret_handlers_group(dp)
other.regisret_handlers_other(dp) 
add_message.regisret_handlers_message(dp)







executor.start_polling(dp, skip_updates=True, on_startup=on_startup) 
