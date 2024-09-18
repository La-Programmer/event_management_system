#!/usr/bin/env python3

from v1.db.engine import storage
from v1.controllers import invitation, event

def get_rsvp_data(invitation_id):
    """Get RSVP data for specific invitation
    """
    try:
        invitation_instance = invitation.get_invitation_by(id=invitation_id)
        event_instance = event.get_event(invitation_instance.event_id)
        rsvp_data = {
            "event_name": event_instance.event_name,
            "recipient_name": invitation_instance.recipient_name,
            "recipient_number": invitation_instance.recipient_number,
            "message": invitation_instance.message
        }
        return rsvp_data
    except Exception:
        raise

def respond_to_iv(invitation_id, response):
    """User response to invitation
    """
    try:
        invitation_instance = invitation.get_invitation_by(id=invitation_id)
        if response:
            updated_iv = invitation.update_invitation(
                invitation_id,
                {"status": "accepted"},
                email=invitation_instance.recipient_email
            )
        else:
            updated_iv = invitation.update_invitation(
                invitation_id,
                {"status": "rejected"},
                email=invitation_instance.recipient_email
            )
        return updated_iv
    except Exception:
        raise

def verify_qrcode(invitation_id, data):
    """Verification of QRcode
    """
    invitation_instance = invitation.get_invitation_by(id=invitation_id)
    name = data.get("recipient_name")
    phone_no = name = data.get("recipient_number")
    if name == invitation_instance.recipient_name and phone_no == invitation_instance.recipient_number:
        return True
    else:
        return False
