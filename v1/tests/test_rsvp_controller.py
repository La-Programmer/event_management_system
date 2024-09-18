#!/usr/bin/env python3
import pytest
from v1.controllers import rsvp, event, invitation

def test_get_rsvp_data(test_invitations):
    """Test getting the rsvp info for an invitation
    """
    try:
        invitation = test_invitations[3]
        invitation_id = invitation.id
        event_instance = event.get_event(invitation.event_id)
        event_name = event_instance.event_name
        recipient_name = invitation.recipient_name
        message = invitation.message
        rsvp_data = rsvp.get_rsvp_data(invitation_id)
        assert rsvp_data.get("recipient_name") == recipient_name
        assert rsvp_data.get("event_name") == event_name
        assert rsvp_data.get("message") == message
    except Exception as e:
        pytest.fail(str(e))

def test_respond_to_iv(test_invitations):
    """Test responding to an invitation
    """
    try:
        invitation1 = test_invitations[2]
        invitation2 = test_invitations[3]
        invitation1_id = invitation1.id
        invitation2_id = invitation2.id
        print(invitation1_id, invitation2_id)
        updated_iv1 = rsvp.respond_to_iv(invitation1_id, True)
        updated_iv2 = rsvp.respond_to_iv(invitation2_id, False)
        print(updated_iv1.to_dict())
        print(updated_iv2.to_dict())
        updated_invitation1 = invitation.get_invitation_by(id=invitation1_id)
        updated_invitation2 = invitation.get_invitation_by(id=invitation2_id)
        assert updated_invitation1.status == "accepted"
        assert updated_invitation2.status == "rejected"
    except Exception as e:
        pytest.fail(str(e))
