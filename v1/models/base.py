#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from db.engine import storage
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """Base class for all classes in the system
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs) -> None:
        """Initialize base class"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.now()
            
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.now()
            
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
    
    def __str__(self):
        """String representation of base class
        """
        return f"{self.__class__.__name__}.{self.id}: {self.__dict__}"
    
    def save_new(self):
        """Saves an object to the DB
        """
        self.updated_at = datetime.now()
        try:
            storage.new(self)
            storage.save()
        except Exception as e:
            raise e
    
    def update(self, **kwargs):
        """Update a DB object
        """
        self.updated_at = datetime.now()
        try:
            storage.update(self, kwargs)
            storage.save()
        except Exception as e:
            raise e
        finally:
            print(self)
    
    def delete(self, obj):
        """Delete a DB object
        """
        try:
            storage.delete(obj)
        except Exception as e:
            raise e
