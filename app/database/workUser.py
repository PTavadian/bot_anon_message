from database.create_db import Session 
from database.models.user import User
from database.cache import redis_client



def add_user_group(user_id: int, group_id: int, title: str):
    '''Добавление группы пользователю при успешной перессылке сообщения'''

    session = Session()
    old_group = session.query(User).filter(User.group_id == group_id).all()
    if not old_group:
        group = User(user_id= user_id,
                     group_id= group_id,
                     title= title)
        session.add(group)
        session.commit()
    session.close()



def get_user_groups(user_id: int) -> list[str]:   
    '''Получение всех названий групп'''

    session = Session()
    groups = session.query(User.title).filter(User.user_id == user_id).all()
    session.close()

    return [gr[0] for gr in groups if groups] if groups else []


