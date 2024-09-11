#!/usr/bin/env python3
"""Invitations model API endpoints
"""

from . import app_views
from ...controllers import invitation
from ...controllers.event import AccessDenied
from celery.result import AsyncResult
from v1.api.celery_tasks import send_invitation
from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

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

@app_views.route('/invitations/<invitation_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_invitation_by_id(invitation_id):
    """Gets an invitation by ID
    """
    try:
        invitation1 = invitation.get_invitation_by(id=invitation_id)
        if invitation1 is None:
            return make_response({'message': 'No invitation was found'}, 404)
        result = invitation1.to_dict()
        return make_response({'message': 'Invitation gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitation', 'exception': str(e)}, 500)

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
        result = [invitation.to_dict() for invitation in invitations]
        return make_response({'message': 'Invitations gotten successfully', 'result': result}, 200)
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
        result = [invitation.to_dict() for invitation in invitations]
        return make_response({'message': 'Invitations gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/invitations_received', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_received_by_a_user():
    """Get all invitations that a user has received
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_invitations_received_by_user(user_id)
        if invitations is None or invitations == []:
            return make_response({'message': f'No invitations were found'}, 404)
        result = [invitation.to_dict() for invitation in invitations]
        return make_response({'message': 'Invitations gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to get invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/invitations_sent', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_invitations_created_by_a_user():
    """Get all invitations created by a user
    """
    user_id = get_jwt_identity()
    try:
        invitations = invitation.get_all_invitations_created_by_user(user_id)
        if invitations is None or invitations == []:
            return make_response({'message': f'No invitations were found'}, 404)
        result = [invitation.to_dict() for invitation in invitations]
        return make_response({'message': 'Invitations gotten successfully', 'result': result}, 200)
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
        invitation.delete_invitation(user_id, invitation_id)
        return make_response({'message': 'Invitation deleted successfully'}, 200)
    except AccessDenied as a:
        return make_response({'message': 'Unauthorized action', 'exception': str(a)}, 401)
    except Exception as e:
        return make_response({'message': 'Failed to delete invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/send_invitation/<invitation_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def send_invitation_endpoint(invitation_id):
    """Send out a single invitation
    """
    try:
        result = send_invitation.delay(invitation_id)
        return make_response({"message": "Email sent successfully", "result": result.id}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to send invitations', 'exception': str(e)}, 500)

@app_views.route('/invitations/monitor_invitations', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_results():
    """Gets the status of sent out invitations
    """
    result_id = request.args.get('result_id')
    result = AsyncResult(result_id)
    if result.ready():
        # Task has completed
        if result.successful():
            return make_response({
                "message": "Email received by user successfully",
                "ready": result.ready(),
                "successful": result.successful(),
                "value": result.result,
            }, 200)
        else:
        # Task completed with an error
            return make_response({'status': 'ERROR', 'error_message': str(result.result)}, 500)
    else:
        # Task is still pending
        return make_response({'status': 'Running'}, 200)
