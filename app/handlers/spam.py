from create_bot import dp, bot
import asyncio

from database.cache import redis_client




async def delete_messages(chat_id: int):
    '''Удаление сообщений'''

    lst = redis_client.lrange(f'del_lst_{chat_id}', 0, 100)
    for msg_id in lst:
        try:
            await asyncio.sleep(0.5)
            await bot.delete_message(chat_id, int(msg_id))
        except Exception as err:
            print(err)
        finally:
            redis_client.delete(f'del_lst_{chat_id}')



