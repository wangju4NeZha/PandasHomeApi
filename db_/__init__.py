from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

engine = create_engine('mysql+pymysql://root:211488@localhost:3306/homems?charset=utf8')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()
