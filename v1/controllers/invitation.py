#!/usr/bin/python3

from v1.db.engine import storage
from v1.models.invitations import Invitation
from .event import AccessDenied
from v1.utils.validate import validate_data

valid_keys = [
        'recipient_id',
        'sender_id',
        'event_id',
        'recipient_name',
        'recipient_number',
        'recipient_email',
        'message',
        'status'
    ]

def get_all_invitations():
    """Get all events from the DB
    """
    try:
        invitations = storage.get_all('Invitation')
        invitation_dict_array = [invitation.to_dict() for invitation in invitations]
        return invitation_dict_array
    except Exception:
        raise

def create_invitation(invitation_info) -> Invitation:
    """Creates an invitation
    """
    try:
        if validate_data(valid_keys, invitation_info):
            new_invitation: Invitation = Invitation(**invitation_info)
            new_invitation.save_new()
            result = get_invitation_by(id=new_invitation.id)
            return result
        else:
            raise Exception('Missing key or invalid key in json data')
    except Exception as e:
        raise

# ALL TYPES OF GETS NEEDED TO HANDLE INVITATIONS
def get_invitation_by(**kwargs) -> Invitation | None:
    """Gets an invitation by the given keyword argument
    """
    try:
        invitation: Invitation = storage.get_object_by('Invitation', **kwargs)
        if invitation is None:
            return None
        return invitation
    except Exception:
        raise

def get_all_invitations_created_by_user(user_id) -> list[Invitation] | None:
    """Gets all invitaitions sent out by a user
    """
    try:
        invitations: list[Invitation] = storage.get_all_by('Invitation', sender_id=user_id)
        if invitations is None or invitations == []:
            return None
        return invitations
    except Exception:
        raise

def get_all_invitations_for_an_event(user_id, event_id) -> list[Invitation] | None:
    """Gets all invitations sent out by an event owner for the event
    """
    try:
        event = storage.get_object_by('Event', id=event_id)
        if event.event_owner != user_id:
            raise AccessDenied('You do not have access to view these invitations')
        invitations: list[Invitation] = storage.get_all_by('Invitation', event_id=event_id)
        if invitations is None or invitations == []:
            return None
        return invitations
    except Exception:
        raise

def get_all_invitations_received_by_user(user_id) -> list[Invitation] | None:
    """Gets all invitations a user has received
    """
    try:
        invitations: list[Invitation] = storage.get_all_by('Invitation', recipient_id=user_id)
        if invitations is None or invitations == []:
            return None
        return invitations
    except Exception:
        raise

def get_all_inviations_for_a_status(user_id, event_id, status) -> list[Invitation] | None:
    """Gets all invitations for an event that have a specific status
    """
    try:
        all_invitations = get_all_invitations_for_an_event(user_id, event_id)
        if all_invitations is None or all_invitations == []:
            return None
        all_accepted_invitations = [invitation for invitation in all_invitations if invitation.status == status]
        return all_accepted_invitations
    except Exception:
        raise

# THE REMAINING CRUD OPERATIONS (UPDATE AND DELETE)

def update_invitation(invitation_id, invitation_info, user_id=None, email=None) -> Invitation:
    """Updated an invitation object
    """
    try:
        if validate_data(valid_keys, invitation_info):
            invitation: Invitation = get_invitation_by(id=invitation_id)
            if invitation is None:
                raise Exception('This invitation does not exist')
            if invitation.sender_id != user_id and invitation.recipient_email != email:
                raise AccessDenied('You do not have access to update this invitation')
            status = invitation_info.get("status")
            if validate_update_status(status):
                invitation.update(**invitation_info)
                updated_invitation = get_invitation_by(id=invitation_id)
                return updated_invitation
            raise ValueError("Invalid value in status key")
        else:
            raise KeyError('Missing key or invalid key in json data')
    except Exception:
        raise

def delete_invitation(user_id, invitation_id) -> None:
    """Delete an invitation object
    """
    try:
        invitation: Invitation = get_invitation_by(id=invitation_id)
        if invitation is None:
            raise Exception('This invitation does not exist')
        if invitation.sender_id != user_id:
            raise AccessDenied('You do not have access to delete this invitation')
        invitation.delete()
        return
    except Exception:
        raise

# UTIL FUNCTIONS
def validate_update_status(status):
    """Valiate the value of the status key in the invitation
    """
    valid_keys = ["pending", "sent", "accepted", "rejected", None]
    if status not in valid_keys:
        return False
    return True
