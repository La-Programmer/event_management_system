#!/usr/bin/python3
"""User model module"""

from .base import BaseModel
from db.engine import Base
from datetime import datetime
import bcrypt
from sqlalchemy import Column, String, DateTime

class User(BaseModel, Base):
    """User model"""
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    phoneNo = Column(String(14), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """Initialize User"""
        super().__init__(*args, **kwargs)
    
    def __setattr__(self, name: str, value) -> None:
        """Sets a password with md5 encryption
        """
        if name == "password":
            try:
                value = value.encode('utf-8')
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(value, salt)
                super().__setattr__(name, hashed_password)
            except Exception as e:
                raise e
        else:
            super().__setattr__(name, value)
