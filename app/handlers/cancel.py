from aiogram import types, Dispatcher 
from create_bot import dp, bot
from aiogram.dispatcher import FSMContext
from handlers.spam import delete_messages



async def cancel_handler(message: types.Message, state: FSMContext):
    '''Выход из состояний'''

    await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove()) 
    await state.finish()
    await delete_messages(message.from_user.id)



def regisret_handlers_cancel(dp : Dispatcher):
    dp.register_message_handler(cancel_handler, state='*', commands='cancel')


