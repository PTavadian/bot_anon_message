from database.create_db import DATABASE_NAME, create_db
import os


def sql_start() -> None:
    '''Создает таблицы в БД'''

    db_is_created = os.path.exists(DATABASE_NAME)
    if not db_is_created:
        create_db()
    print('Data base connect OK!')


