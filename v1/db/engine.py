#!/usr/bin/env python3
"""DB Module
"""

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import os


load_dotenv()
Base = declarative_base()
classes = {
    # 'User': User,
    # 'Event': Event,
    # 'Invitation': Invitation
}
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
        env = os.environ.get('ENV')
        db = os.environ.get('DB')
        self.__engine = create_engine(f"mysql+mysqldb://{user}:{pwd}@{host}/{db}")
    
    def get_object_by(self, obj_class_str, **kwargs):
        """Gets an object from the DB by a particular attribute
        """
        obj_class = classes[obj_class_str]
        db_session = self._session
        raw_columns = obj_class.__table__.columns
        columns = [str(field).split('.')[1] for field in raw_columns]
        for i in kwargs:
            if i not in columns:
                raise InvalidRequestError
        user = db_session.query(obj_class).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user


    def save(self):
        """Commit all changes of the current DB session
        """
        try:
            self.__session.commit()
            print('Object save successfully')
        except Exception as e:
            raise e
            
    def new(self, new_obj):
        """Adds a new object to the session DB
        """
        try:
            self.__session.add(new_obj)
        except Exception as e:
            raise e
    
    def update(self, obj, kwargs):
        """Updates a DB record
        """
        name = obj.__class__.__name__
        class_name = classes[name]
        instance_object = self.__session.query(class_name).filter_by(obj.id).first()
        for key, value in kwargs.items():
            try:
                setattr(instance_object, key, value)
            except Exception as e:
                raise e


    def reload(self):
        """Reloads data from the DB
        """
        try:
            Base.metadata.create_all(self.__engine)
            sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
            Session = scoped_session(sess_factory)
            self.__session = Session
        except Exception as e:
            raise e
    
    def is_alive(self):
        """Confirm that connecting to DB was successful
        """
        if self.__session and self.__engine:
            return True
        return False
    
    def delete(self, obj):
        """Delete from DB
        """
        if obj is not None:
            try:
                self.__session.delete(obj)
            except Exception as e:
                raise e
        else:
            raise ValueError('No object to delete')
    
    def close(self):
        """Call remove() method on the private session attribute
        """
        try:
            self.__session.remove()
        except Exception as e:
            raise e
