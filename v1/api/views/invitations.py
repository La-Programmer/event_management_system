#!/usr/bin/env python3
"""Invitations model API endpoints
"""

from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...controllers import invitation
from ...controllers.event import AccessDenied
from . import app_views

@app_views.route('/invitations', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations():
    """Get all invitations endpoint
    """
    try:
        invitations = invitation.get_all_invitations()
        if invitations is None or invitations == []:
            return make_response({'message': 'No invitations were found'}, 404)
        return make_response({'message': 'Invitations gotten successfully', 'result': invitations}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/event/<event_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_for_an_event(event_id):
    """Get all invitations sent out by a user for an event endpoint
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_invitations_for_an_event(user_id, event_id)
        if invitations is None or invitations == []:
            return make_response({'message': 'No invitations were found'}, 404)
        return make_response({'message': 'Invitations gotten successfully', 'result': invitations}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(a)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/event/<event_id>/<status>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_for_an_event_by_status(event_id, status):
    """Get all invitations for an event according to the given status endpoint
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_inviations_for_a_status(user_id, event_id, status)
        if invitations is None or invitations == []:
            return make_response({'message': f'No invitations were found with status {status}'}, 404)
        return make_response({'message': 'Invitations gotten successfully', 'result': invitations}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/invitations_received/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_received_by_a_user(user_id):
    """Get all invitations that a user has received
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_invitations_received_by_user(user_id)
        if invitations is None or invitations == []:
            return make_response({'message': f'No invitations were found'}, 404)
        return make_response({'message': 'Invitations gotten successfully', 'result': invitations}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/invitations_sent/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_created_by_a_user(user_id):
    """Get all invitations created by a user
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_invitations_created_by_user(user_id)
        if invitations is None or invitations == []:
            return make_response({'message': f'No invitations were found'}, 404)
        return make_response({'message': 'Invitations gotten successfully', 'result': invitations}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_invitation():
    """Create a new invitation
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        data['sender_id'] = user_id
        new_invitation = invitation.create_invitation(data)
        result = new_invitation.to_dict()
        return make_response({'message': 'Invitation created successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to create invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/<invitation_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_invitation(invitation_id):
    """Update an existing invitation
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        updated_invitation = invitation.update_invitation(user_id, invitation_id, data)
        result = updated_invitation.to_dict()
        return make_response({'message': 'Invitation updated successfully', 'result': result}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(a)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to create invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/<invitation_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_invitation(invitation_id):
    """Update an existing invitation
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        invitation.delete_invitation(user_id, invitation_id, data)
        return make_response({'message': 'Invitation deleted successfully'}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(a)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to create invitations', 'exception': str(e)}, 500)

