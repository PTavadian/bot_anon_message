import sqlite3 as sq
import datetime
import json





def sql_start() -> None:
    '''Создает таблицы в БД'''
    global base, cur
    base = sq.connect('shame.db')
    cur = base.cursor()
    if base:
        print('Data base connect OK!')

    base.execute('''CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        title TEXT,
        time TEXT,
        status TEXT
        )''')
    
    base.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT,
        list_group TEXT
        )''')

    base.commit()







def append_group(group_id: int, title: str, status: str='active') -> None:
    '''Записывает в БД id и название группы'''

    time = datetime.datetime.now()
    time = time.strftime("%d/%m/%Y  %H:%M:%S")

    try:
        cur.execute(f"INSERT INTO groups VALUES('{group_id}', '{title}', '{time}', '{status}')")
        base.commit()
    except sq.IntegrityError:
        cur.execute(f"UPDATE groups SET status = '{status}' WHERE group_id == '{group_id}'")
        base.commit()
    except:
        print('Ошибка при работе с БД ----append_group----')







def get_id_group(titles: str) -> str:
    '''Возвращает id группы по названию'''

    titles = [titles]
    titles.append(' ')
    titles = tuple(titles)
    
    cur.execute(f"SELECT group_id FROM groups WHERE title IN {titles} ORDER BY time DESC")
    result = cur.fetchone()

    return result







def append_user(user_id: int, first_name: str, last_name: str, username: str, list_group: list) -> None:
    '''Добавляет нового пользователя в БД или бобавляет к нему название новой группы'''

    cur.execute(f"SELECT list_group FROM users WHERE user_id == {user_id}")
    old_list: list = cur.fetchone()

    if old_list:
        old_list = json.loads(*old_list) #возвращает список
        old_list = set(old_list)        
        lst = {list_group}
        list_group = old_list | lst
    else:
        list_group = {list_group}
        
    list_group = list(list_group)
    list_group = json.dumps(list_group) #возвращает json


    try:
        cur.execute(f"INSERT INTO users VALUES('{user_id}', '{first_name}', '{last_name}', '{username}', '{list_group}')")
        base.commit()
    except sq.IntegrityError:
        cur.execute(f"UPDATE users SET list_group = '{list_group}' WHERE user_id == '{user_id}'")
        base.commit()
    except:
        print('Ошибка при работе с БД ----append_user----')







def get_list_group(user_id: int) -> list:
    '''Возвращает список групп'''

    cur.execute(f"SELECT list_group FROM users WHERE user_id == {user_id}")
    result = cur.fetchone()
    if result:
        result = json.loads(*result)
    return result







def del_name_group(user_id: int, name: str) -> None:
    '''Удаляет группу из БД'''

    cur.execute(f"SELECT list_group FROM users WHERE user_id == {user_id}")
    lst = cur.fetchone()
    lst = json.loads(*lst)
    try:
        lst.remove(name)
        lst = json.dumps(lst) #возвращает json
        cur.execute(f"UPDATE users SET list_group = '{lst}' WHERE user_id == '{user_id}'")
        base.commit()
    except:
        print('Ошибка при работе с БД ----del_name_group----') 
    return None
    
















 

 
