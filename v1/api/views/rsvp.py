#!/usr/bin/env python3
"""API endpoints to handle RSVP process
"""

from . import app_views
from ...controllers import rsvp
from flask import request, make_response
from flask_jwt_extended import jwt_required

@app_views.route("/rsvp/<invitation_id>", methods=['GET'], strict_slashes=False)
def get_rsvp_data(invitation_id):
    """Get RSVP data
    """
    try:
        result = rsvp.get_rsvp_data(invitation_id)
        return make_response({"message": "RSVP data gotten successfully", "result": result}, 200)
    except Exception as e:
        return make_response({"message": "Error getting RSVP data", "exception": str(e)}, 500)

@app_views.route("/rsvp/<invitation_id>", methods=["POST"], strict_slashes=False)
def rsvp_to_iv(invitation_id):
    """Invitees response to invitation
    """
    try:
        data = request.get_json()
        user_response = data.get("status")
        if user_response == "true" or user_response == "True":
            response = True
        else:
            response = False
        rsvp.respond_to_iv(invitation_id, response)
        return make_response({"message": "Successfully responded to IV"}, 200)
    except Exception as e:
        return make_response({"message": "Error responding to IV", "exception": str(e)}, 500)

@app_views.route("/verify_qrcode/<invitation_id>/<event_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def verify_qrcode(invitation_id, event_id):
    """Verify an invitees QRcode
    """
    try:
        if rsvp.verify_qrcode(invitation_id, event_id):
            return make_response({"message": "User is verified"}, 200)
        else:
            return make_response({"message": "This user is not invited"}, 202)
    except Exception as e:
        return make_response({"message": "Error verifying user", "exception": str(e)}, 500)
