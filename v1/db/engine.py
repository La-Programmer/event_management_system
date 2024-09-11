#!/usr/bin/env python3
"""DB Module
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from ..utils.get import get_classes


class DB(SQLAlchemy):
    """Handle MySQL DB connection"""
    def get_object_by(self, obj_class_str, **kwargs):
        """Gets an object from the DB by a particular attribute
        """
        obj_class = get_classes(obj_class_str)
        db_session = self.session
        raw_columns = obj_class.__table__.columns
        columns = [str(field).split('.')[1] for field in raw_columns]
        for i in kwargs:
            if i not in columns:
                raise InvalidRequestError
        obj = db_session.query(obj_class).filter_by(**kwargs).first()
        if obj is None:
            raise NoResultFound
        return obj

    def get_all(self, obj_class_str):
        """Gets all instances of a model from the DB
        """
        obj_class = get_classes(obj_class_str)
        db_session = self.session
        try:
            objs = db_session.query(obj_class).all()
            return objs
        except Exception as e:
            raise e

    def get_all_by(self, obj_class_str, **kwargs):
        """Get all instances of an object that match the keyword argument
        """
        obj_class = get_classes(obj_class_str)
        db_session = self.session
        raw_columns = obj_class.__table__.columns
        columns = [str(field).split('.')[1] for field in raw_columns]
        for i in kwargs:
            if i not in columns:
                raise InvalidRequestError
        obj = db_session.query(obj_class).filter_by(**kwargs).all()
        if obj is None:
            raise NoResultFound
        return obj

    def save(self):
        """Commit all changes of the current DB session
        """
        db_session = self.session
        try:
            db_session.commit()
            print('Object saved successfully')
        except Exception as e:
            raise e
            
    def new(self, new_obj):
        """Adds a new object to the session DB
        """
        db_session = self.session
        try:
            db_session.add(new_obj)
        except Exception as e:
            raise e
    
    def update(self, obj, kwargs):
        """Updates a DB record
        """
        name = obj.__class__.__name__
        class_name = get_classes(name)
        instance_object = self.get_object_by(class_name, id=obj.id)
        for key, value in kwargs.items():
            try:
                setattr(instance_object, key, value)
            except Exception as e:
                raise e


    # def reload(self):
    #     """Reloads data from the DB
    #     """
    #     try:
    #         Base.metadata.create_all(self.__engine)
    #         sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
    #         Session = scoped_session(sess_factory)
    #         self.__session = Session
    #     except Exception as e:
    #         raise e
    
    def is_alive(self):
        """Confirm that connecting to DB was successful
        """
        if self.session:
            return True
        return False
    
    def delete(self, obj):
        """Delete from DB
        """
        db_session = self.session
        if obj is not None:
            try:
                db_session.delete(obj)
                self.save()
                print('Deleted successfully')
            except Exception as e:
                raise e
        else:
            raise ValueError('No object to delete')
    
    def close(self):
        """Call remove() method on the private session attribute
        """
        db_session = self.session
        try:
            db_session.remove()
        except Exception as e:
            raise e

storage = DB()

# try:
#     storage.reload()
# except Exception as e:
#     raise e

def init_db(app):
    storage.init_app(app)

