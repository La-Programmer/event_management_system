#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from db import storage
import uuid

class BaseModel:
    """Base class for all classes in the system
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __init__(self) -> None:
        print('New base instance')
        storage.is_alive()
