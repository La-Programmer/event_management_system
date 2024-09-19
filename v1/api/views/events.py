#!/usr/bin/env python3
"""Event model API endpoints
"""
from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...controllers import event
from ...controllers.event import AccessDenied
from . import app_views

@app_views.route('/events/<event_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_event(event_id):
    """Get an event from DB
    """
    try:
        event_instance = event.get_event(event_id)
        if event_instance is None:
            return make_response({'message': 'No event was found'}, 404)
        result = event_instance.to_dict()
        return make_response({'message': f'Event {event_instance.event_name} gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get events', 'exception': str(e)}, 500)

@app_views.route('/events/your_events', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_events():
    """Get all events for a user from the DB
    """
    try:
        user_id = get_jwt_identity()
        print(user_id)
        events = event.get_events_by_owner(user_id)
        if events is None or events == []:
            return make_response({'message': 'No events were found for this user'}, 404)
        result = [event_instance.to_dict() for event_instance in events]
        return make_response({'message': 'Events gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get events', 'exception': str(e)}, 500)

@app_views.route('/events/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_event():
    """Create an event
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        data['event_owner'] = user_id
        new_event = event.create_event(data)
        result = new_event.to_dict()
        return make_response({'message': 'Event created successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to create new event', 'exception': str(e)}, 500)

@app_views.route('/events/update/<event_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_event(event_id):
    """Update an event
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        updated_event = event.update_event(event_id, user_id, data)
        result = updated_event.to_dict()
        return make_response({'message': f'Event {updated_event.event_name} updated successfully', 'result': result}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(e)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to update event', 'exception': str(e)}, 500)

@app_views.route('/events/delete/<event_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_event(event_id):
    """Delete an event
    """
    try:
        user_id = get_jwt_identity()
        event.delete_event(event_id, user_id)
        return make_response({'message': 'Event deleted successfully'}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(e)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to delete event', 'exception': str(e)}, 500)
