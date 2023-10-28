from sqlalchemy import Column, Integer, String, DateTime, BigInteger, BOOLEAN
from database.create_db import Base
from datetime import datetime


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, autoincrement=True, primary_key=True)
    group_id = Column(BigInteger, unique=False)
    title = Column(String)
    status = Column(BOOLEAN, default=False)  
    registration_date = Column(DateTime, default=datetime.now()) 
    update_date = Column(DateTime, onupdate=datetime.now())


    def __init__(self, group_id: BigInteger,
                 title: String, 
                 status: BOOLEAN=False,
                 registration_date: DateTime=None,
                 update_date: DateTime=None):


        self.group_id = group_id
        self.title = title
        self.status = status
        self.registration_date = registration_date
        self.update_date = update_date




