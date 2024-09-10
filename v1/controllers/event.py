#!/usr/bin/env python3

from v1.db.engine import storage
from v1.models.events import Event
from v1.utils.validate import validate_data
from sqlalchemy.orm.exc import NoResultFound

valid_keys = ['event_owner', 'event_name', 'event_location', 'date_time']

# CUSTOM EXCEPTION FOR ACCESS DENIAL
class AccessDenied(Exception):
    """Access denied exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"Access Denied: {self.message}"

def create_event(event_info) -> Event:
    """Creates an event
    """
    try:
        if validate_data(valid_keys, event_info):
            new_event: Event = Event(**event_info)
            new_event.save_new()
            return new_event
        else:
            raise Exception('Missing key or invalid key in json data')
    except Exception as e:
        raise

def get_event(event_id) -> Event | None:
    """Gets an event
    """
    try:
        event = storage.get_object_by('Event', id=event_id)
        if event is None:
            return None
        return event
    except NoResultFound:
        return None
    except Exception:
        raise

def get_events_by_owner(owner_id) -> list[Event] | None:
    """Gets an event owned by a specific user
    """
    try:
        events = storage.get_all_by('Event', event_owner=owner_id)
        if events is None:
            return None
        return events
    except Exception:
        raise

def update_event(event_id, user_id, event_info) -> Event:
    """Updates an event
    """
    try:
        if validate_data(valid_keys, event_info):
            event: Event = get_event(event_id)
            if event is None:
                raise Exception('This event does not exist')
            if event.event_owner == user_id:
                event.update(**event_info)
                updated_event = get_event(event_id)
                return updated_event
            raise AccessDenied('You are not authorized to update this event')
        else:
            raise Exception('Missing key or invalid key in json data')
    except Exception:
        raise

def delete_event(event_id, user_id) -> None:
    """Deletes an event
    """
    try:
        event = get_event(event_id)
        if event is None:
            raise Exception('This event does not exist')
        if event.event_owner == user_id:
            event.delete()
            return
        raise AccessDenied('You are not authorized to delete this event')
    except Exception as e:
        raise
