#!/usr/bin/python3

from .base import BaseModel
from ..db.engine import storage
from sqlalchemy import Column, String, ForeignKey

class Invitation(BaseModel, storage.Model):
    """Invitation model
    """
    recipient_id = Column(String(128), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    sender_id = Column(String(128), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    event_id = Column(String(128), ForeignKey('event.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    recipient_name = Column(String(128), nullable=False)
    recipient_number = Column(String(128), nullable=False)
    recipient_email = Column(String(128), nullable=False)
    message = Column(String(128), nullable=False)
    status = Column(String(10), default='pending')

    def __init__(self, *args, **kwargs):
        """Initialize Invitation"""
        status = kwargs.get('status')
        if status is None:
            kwargs["status"] = 'pending'
        super().__init__(*args, **kwargs)
