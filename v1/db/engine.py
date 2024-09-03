#!/usr/bin/env python3
"""DB Module
"""

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


load_dotenv()
Base = declarative_base()
class DB:
    """Handle MySQL DB connection"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        user = os.environ.get('USER')
        pwd = os.environ.get('PASS')
        host = os.environ.get('HOST')
        db = os.environ.get('DB')
        # env = os.environ.get('ENV')
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{pwd}@{host}/{db}")

    def save(self):
        """Commit all changes of the current DB session
        """
        self.__session.commit()
    
    def reload(self):
        """Reloads data from the DB
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        print('Database is up and running')
    
    def is_alive(self):
        """Confirm that connecting to DB was successful
        """
        if self.__session and self.__engine:
            print('DB connected and ready to go')
    
    def close(self):
        """Call remove() method on the private session attribute
        """
        self.__session.remove()
