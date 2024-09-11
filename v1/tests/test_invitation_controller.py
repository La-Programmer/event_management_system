#!/usr/bin/env python3

import pytest
from datetime import datetime
from v1.controllers import invitation
from v1.controllers.event import AccessDenied
from sqlalchemy.exc import NoResultFound

def test_get_all_invitations(test_invitations):
    """Test getting all invitations from the DB
    """
    try:
        invitations = invitation.get_all_invitations()
        assert invitations is not None
        assert len(invitations) == 5
    except Exception as e:
        pytest.fail(str(e))

def test_get_invitations_by(create_test_users, test_invitations, test_events):
    """Test getting an invitation by any keyword argument
    """
    try:
        invitation1 = invitation.get_invitation_by(id=test_invitations[0].id)
        invitation2 = invitation.get_invitation_by(id=test_invitations[1].id)
        invitation3 = invitation.get_invitation_by(id=test_invitations[2].id)
        invitation4 = invitation.get_invitation_by(id=test_invitations[3].id)
        assert invitation1.id == test_invitations[0].id
        assert invitation2.id == test_invitations[1].id
        assert invitation3.id == test_invitations[2].id
        assert invitation4.id == test_invitations[3].id
        invitation1_by_name = invitation.get_invitation_by(recipient_name=create_test_users[0].get_fullname())
        invitation2_by_email = invitation.get_invitation_by(recipient_email=create_test_users[1].email)
        invitation3_by_event = invitation.get_invitation_by(event_id=test_events[4].id)
        invitation4_by_recipient_id = invitation.get_invitation_by(recipient_id=create_test_users[3].id)
        assert invitation1_by_name.id == test_invitations[0].id
        assert invitation2_by_email.id == test_invitations[1].id
        assert invitation3_by_event.id == test_invitations[2].id
        assert invitation4_by_recipient_id.id == test_invitations[3].id
    except Exception as e:
        pytest.fail(str(e))

def test_create_invitation(create_test_users, test_events):
    """Test creating an invitation
    """
    data = {
        'recipient_id': create_test_users[4].id,
        'sender_id': create_test_users[len(create_test_users) - 1].id,
        'event_id': test_events[1].id,
        'recipient_name': create_test_users[4].get_fullname(),
        'recipient_number': create_test_users[4].phoneNo,
        'recipient_email': create_test_users[4].email,
        'message': 'You are invited to my random event',
    }
    try:
        new_invitation = invitation.create_invitation(data)
        new_iv_from_db = invitation.get_invitation_by(id=new_invitation.id)
        assert new_invitation.id == new_iv_from_db.id
        assert new_invitation.recipient_id == new_iv_from_db.recipient_id
        assert new_invitation.sender_id == new_iv_from_db.sender_id
        assert new_invitation.event_id == new_iv_from_db.event_id
        assert new_invitation.recipient_name == new_iv_from_db.recipient_name
        assert new_invitation.recipient_number == new_iv_from_db.recipient_number
        assert new_invitation.recipient_email == new_iv_from_db.recipient_email
        assert new_invitation.message == new_iv_from_db.message
        new_invitation.delete()
    except Exception as e:
        pytest.fail(str(e))

def test_get_all_invitations_created_by_user(create_test_users):
    """Test getting all invitations by a user
    """
    user_id = create_test_users[5].id
    try:
        invitations = invitation.get_all_invitations_created_by_user(user_id)
        assert len(invitations) == 5
        invitation1 = invitations[0]
        invitation2 = invitations[1]
        invitation3 = invitations[2]
        invitation4 = invitations[3]
        assert invitation1.sender_id == invitation2.sender_id
        assert invitation2.sender_id == invitation3.sender_id
        assert invitation3.sender_id == invitation4.sender_id
    except Exception as e:
        pytest.fail(str(e))

def test_all_invitations_received_by_user(create_test_users):
    """Test getting all invitations received by a user
    """
    user_id = create_test_users[0].id
    try:
        invitations = invitation.get_all_invitations_received_by_user(user_id)
        assert len(invitations) == 1
        invitation1 = invitations[0]
        assert invitation1.recipient_id == user_id
    except Exception as e:
        pytest.fail(str(e))

def test_get_all_invitations_for_an_event_unauthorised(create_test_users, test_events):
    """Test getting all invitations sent out by an unauthorized user for an event
    """
    user_id = create_test_users[5].id
    event_id = test_events[0].id
    try:
        with pytest.raises(AccessDenied):
            invitations = invitation.get_all_invitations_for_an_event(user_id, event_id)
    except Exception as e:
        pytest.fail(str(e))

def test_get_all_invitations_for_an_event(create_test_users, test_events):
    """Test getting all invitations sent out by a user for an event
    """
    user_id = create_test_users[0].id
    event_id = test_events[1].id
    data = [
        {
            'recipient_id': create_test_users[2].id,
            'sender_id': user_id,
            'event_id': test_events[1].id,
            'recipient_name': create_test_users[2].get_fullname(),
            'recipient_number': create_test_users[2].phoneNo,
            'recipient_email': create_test_users[2].email,
            'message': 'You are invited to my random event',
        },
        {
            'recipient_id': create_test_users[4].id,
            'sender_id': user_id,
            'event_id': test_events[1].id,
            'recipient_name': create_test_users[4].get_fullname(),
            'recipient_number': create_test_users[4].phoneNo,
            'recipient_email': create_test_users[4].email,
            'message': 'You are invited to my random event',
        }
    ]
    try:
        for iv_data in data:
            invitation.create_invitation(iv_data)
        invitations = invitation.get_all_invitations_for_an_event(user_id, event_id)
        assert len(invitations) == 2
        invitation1 = invitations[0]
        invitation2 = invitations[1]
        assert invitation1.sender_id == invitation2.sender_id 
        assert invitation1.event_id == invitation2.event_id
    except Exception as e:
        pytest.fail(str(e))

def test_get_all_invitations_received_by_user(create_test_users, test_events):
    """Test getting invitations for an event created by user, using the status of the invitations
    """
    user_id = create_test_users[0].id
    event_id = test_events[1].id
    try:
        invitations_pending = invitation.get_all_inviations_for_a_status(user_id, event_id, 'pending')
        assert len(invitations_pending) == 2
        invitations_sent = invitation.get_all_inviations_for_a_status(user_id, event_id, 'sent')
        invitations_accepted = invitation.get_all_inviations_for_a_status(user_id, event_id, 'accepted')
        invitations_rejected = invitation.get_all_inviations_for_a_status(user_id, event_id, 'rejected')
        assert len(invitations_sent) == 0
        assert len(invitations_accepted) == 0
        assert len(invitations_rejected) == 0
    except Exception as e:
        pytest.fail(str(e))

def test_update_invitation(create_test_users, test_invitations):
    """Test updating an invitation
    """
    data = {
        'recipient_name': 'Hon. Ashibuogwu and Family',
        'message': 'It is my honour to invite you for my wedding as the chairman of the occassion'
    }
    invitation_id = test_invitations[3].id
    user_id = create_test_users[5].id
    try:
        updated_invitation = invitation.update_invitation(user_id, invitation_id, data)
        assert updated_invitation.recipient_name == 'Hon. Ashibuogwu and Family'
        assert updated_invitation.message == 'It is my honour to invite you for my wedding as the chairman of the occassion'
    except Exception as e:
        pytest.fail(str(e))

def test_delete_invitation(create_test_users, test_invitations):
    """Test deleting an invitation
    """
    invitation_id = test_invitations[0].id
    user_id = create_test_users[5].id
    try:
        invitation.delete_invitation(user_id, invitation_id)
        with pytest.raises(NoResultFound):
            invitation.get_invitation_by(id=invitation_id)
    except Exception as e:
        pytest.fail(str(e))
