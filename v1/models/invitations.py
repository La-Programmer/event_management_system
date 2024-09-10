#!/usr/bin/python3

from .base import BaseModel
from ..db.engine import storage
from sqlalchemy import Column, String, DateTime, ForeignKey

class Invitation(BaseModel, storage.Model):
    """The Invitation model
    """
    recipient_id = Column(String(128), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    sender = Column(String(128), ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    event_id = Column(String(128), ForeignKey('event.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    recipient_name = Column(String(128), nullable=False)
    recipient_number = Column(String(128), nullable=False)
    recipient_email = Column(String(128), nullable=False)
    message = Column(String(128), nullable=False)
    status = Column(String(10), default='pending')

    def __init__(self, *args, **kwargs):
        """Initialize User"""
        try:
            status = kwargs['status']
            self.validate_status(status)
            super().__init__(*args, **kwargs)
        except Exception:
            raise

    def validate_status(self, status) -> None:
        """Validate the value coming in for invitation status
        """
        valid_values = ['pending', 'accepted', 'rejected']
        if status not in valid_values:
            raise ValueError('Invalid value for invitation attribute "status"')
        return
