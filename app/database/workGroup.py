from database.create_db import Session 
from database.models.group import Group
from database.cache import redis_client



def add_group(group_id: int, title: str, status: bool=False):   
    '''Добавление группы и активация группы командой /add'''

    session = Session()
    group = session.query(Group).filter(Group.group_id == group_id).all()
    if group:
        session.query(Group).filter(Group.group_id == group_id).update({Group.status: status, Group.title: title,})
    
    else:
        group = Group(group_id= group_id,
                      title= title,
                      status= status)
        session.add(group)
    session.commit()
    session.close()



def update_status(group_id: int, status: bool=True):
    '''Одновление статуса группы'''

    session = Session()
    session.query(Group).filter(Group.group_id == group_id).update({Group.status: status})
    session.commit()
    session.close()



def get_group(title: str) -> int:   
    '''Получение id группы'''


    session = Session()
    group_id = session.query(Group.group_id).filter((Group.status == True) & (Group.title == title)).all()

    session.close()

    return group_id[0][0] if group_id else False



def delete_group(group_id: int):   
    '''Удаление группы'''

    session = Session()
    session.query(Group).filter(Group.user_id == group_id).delete()
    session.commit()
    session.close()

