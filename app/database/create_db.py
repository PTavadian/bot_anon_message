from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import IS_DOCKER


folder = '' if IS_DOCKER else 'app/'
DATABASE_NAME = f'{folder}database/db/shame.db'


engine = create_engine(f'sqlite:///{DATABASE_NAME}') #, echo=True)
Session = sessionmaker(bind=engine) 
Base = declarative_base()

def create_db():
    Base.metadata.create_all(engine)





