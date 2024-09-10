#!/usr/bin/python3
"""User model module"""

from .base import BaseModel
from ..db.engine import storage
from sqlalchemy import Column, String, DateTime, ForeignKey

class Event(BaseModel, storage.Model):
    """Event model
    """
    event_owner = Column(String(128), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    event_name = Column(String(128), nullable=False)
    event_location = Column(String(128), nullable=False)
    date_time = Column(DateTime, nullable=False)
    invitation_link = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize User"""
        super().__init__(*args, **kwargs)
