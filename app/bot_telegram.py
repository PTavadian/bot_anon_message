from aiogram.utils import executor
from database import db
from create_bot import dp


from create_bot import dp


async def on_startup(_):
    db.sql_start()


from handlers import other, cancel, shame, add_group


cancel.regisret_handlers_cancel(dp)
other.regisret_handlers_other(dp)
add_group.regisret_handlers_group(dp)
shame.regisret_handlers_shame(dp) 



executor.start_polling(dp, skip_updates=True, on_startup=on_startup) 
