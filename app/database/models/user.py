from sqlalchemy import Column, Integer, String, DateTime, BigInteger, BOOLEAN
from database.create_db import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)      
    user_id = Column(BigInteger, unique=True)   # id телеграма
    group_id = Column(BigInteger, unique=False)
    title = Column(String)
    status = Column(BOOLEAN, default=True)  
    registration_date = Column(DateTime, default=datetime.now()) 
    update_date = Column(DateTime, onupdate=datetime.now())


    def __init__(self, user_id: BigInteger,
                 group_id: BigInteger,
                 title: String, 
                 status: BOOLEAN=True,
                 registration_date: DateTime=None,
                 update_date: DateTime=None):


        self.user_id = user_id
        self.group_id = group_id
        self.title = title
        self.status = status
        self.registration_date = registration_date
        self.update_date = update_date




