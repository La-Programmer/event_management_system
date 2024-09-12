#!/usr/bin/env python3
import json
from v1.controllers import invitation

def test_create_invitation(test_client, json_web_token, test_event_for_iv, create_test_users):
    """Test create invitation
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'recipient_id': create_test_users[0].id,
        'sender_id': user['id'],
        'event_id': test_event_for_iv.id,
        'recipient_name': create_test_users[0].get_fullname(),
        'recipient_number': create_test_users[0].phoneNo,
        'recipient_email': create_test_users[0].email,
        'message': 'You are invited to my product launch',
    }
    response = test_client.post('/v1/api/invitations', headers=headers, data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    loaded_response = json.loads(response.data)
    assert loaded_response['message'] == 'Invitation created successfully'

def test_get_an_invitation_endpoint(test_client, json_web_token):
    """Test the endpoint that gets an invitation by ID
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/invitations/invitations_sent', headers=headers)
    loaded_response = json.loads(response.data)
    assert response.status_code == 200
    assert len(loaded_response["result"]) == 1
    invitation1 = loaded_response["result"][0]
    invitation_id = invitation1["id"]
    response2 = test_client.get(f'/v1/api/invitations/{invitation_id}', headers=headers)
    assert response2.status_code == 200
    loaded_response2 = json.loads(response.data)
    assert loaded_response2['message'] == 'Invitations gotten successfully'
    invitation2 = loaded_response2["result"][0]
    assert invitation1 == invitation2

def test_get_all_invitations_endpoint(test_client, json_web_token):
    """Test get all invitations endpoint
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get('/v1/api/invitations', headers=headers)
    loaded_response = json.loads(response.data)
    print(loaded_response)
    assert response.status_code == 200
    assert loaded_response['message'] == 'Invitations gotten successfully'
    assert len(loaded_response['result']) == 7

def test_get_all_invitations_endpoint_unauthorized(test_client):
    """Test get all invitations endpoint with unauthorized user
    """
    response = test_client.get('/v1/api/invitations')
    loaded_response = json.loads(response.data)
    assert response.status_code == 401
    assert loaded_response['msg'] == 'Missing Authorization Header'

def test_get_all_invitations_for_an_event(test_client, json_web_token, test_event_for_iv):
    """Test get all invitations for an event
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_id = test_event_for_iv.id
    response = test_client.get(f'/v1/api/invitations/event/{event_id}', headers=headers)
    loaded_response = json.loads(response.data)
    print(loaded_response)
    assert response.status_code == 200
    assert loaded_response['message'] == 'Invitations gotten successfully'
    assert len(loaded_response['result']) == 1

def test_get_all_invitations_for_an_event_by_status(test_client, json_web_token, test_event_for_iv):
    """Test get all invitations for an event by the invitation status
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_id = test_event_for_iv.id
    response = test_client.get(f'/v1/api/invitations/event/{event_id}/pending', headers=headers)
    assert response.status_code == 200
    loaded_response = json.loads(response.data)
    assert loaded_response['message'] == 'Invitations gotten successfully'
    assert len(loaded_response['result']) == 1
    response1 = test_client.get(f'/v1/api/invitations/event/{event_id}/sent', headers=headers)
    response2 = test_client.get(f'/v1/api/invitations/event/{event_id}/accepted', headers=headers)
    response3 = test_client.get(f'/v1/api/invitations/event/{event_id}/rejected', headers=headers)
    assert response1.status_code == 404
    loaded_response1 = json.loads(response1.data)
    assert loaded_response1['message'] == 'No invitations were found with status sent'
    assert response2.status_code == 404
    loaded_response2 = json.loads(response2.data)
    assert loaded_response2['message'] == 'No invitations were found with status accepted'
    assert response3.status_code == 404
    loaded_response3 = json.loads(response3.data)
    assert loaded_response3['message'] == 'No invitations were found with status rejected'

def test_get_all_invitations_received_by_a_user(test_client, json_web_token):
    """Test get all invitations that have been received by a user
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/invitations/invitations_received', headers=headers)
    assert response.status_code == 200
    loaded_response = json.loads(response.data)
    assert loaded_response['message'] == 'Invitations gotten successfully'
    assert len(loaded_response['result']) == 1

def test_get_all_invitations_created_by_a_user(test_client, json_web_token):
    """Test get all invitations created by a user
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/invitations/invitations_received', headers=headers)
    assert response.status_code == 200
    loaded_response = json.loads(response.data)
    assert loaded_response['message'] == 'Invitations gotten successfully'
    assert len(loaded_response['result']) == 1

def test_update_invitation(test_client, json_web_token, create_test_users, test_event_for_iv):
    """Test updating an invitation
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'recipient_id': create_test_users[1].id,
        'sender_id': user['id'],
        'event_id': test_event_for_iv.id,
        'recipient_name': create_test_users[1].get_fullname(),
        'recipient_number': create_test_users[1].phoneNo,
        'recipient_email': create_test_users[1].email,
        'message': 'You are invited to my product launch',
    }
    response = test_client.post('/v1/api/invitations', headers=headers, data=json.dumps(data), content_type='application/json')
    loaded_response = json.loads(response.data)
    print("Loaded response", loaded_response)
    invitation_info = loaded_response['result']
    invitation_id = invitation_info['id']
    update_data = {
        'message': 'You are specially invited to my product launch as the chairman of the occassion'
    }
    response2 = test_client.put(f'/v1/api/invitations/{invitation_id}', headers=headers, data=json.dumps(update_data), content_type='application/json')
    assert response2.status_code == 200
    loaded_response2 = json.loads(response2.data)
    print("Loaded response 2", loaded_response2)
    assert loaded_response2['message'] == 'Invitation updated successfully'
    assert loaded_response2['result']['message'] == update_data['message']

def test_send_invitation(test_client, json_web_token):
    """Test send invitation endpoint
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/invitations/invitations_sent', headers=headers)
    loaded_response = json.loads(response.data)
    assert response.status_code == 200
    assert len(loaded_response["result"]) == 2
    invitation1 = loaded_response["result"][0]
    invitation_id = invitation1["id"]
    response2 = test_client.post(f"/v1/api/invitations/send_invitation/{invitation_id}", headers=headers)
    loaded_response2 = json.loads(response2.data)
    print(loaded_response2)
    print(invitation_id)
    assert response2.status_code == 200
    assert loaded_response2["message"] == "Email sent successfully"
    result_id = loaded_response2["result"]
    response3 = test_client.get(f"/v1/api/invitations/monitor_invitations?result_id={result_id}", headers=headers)
    assert response3.status_code == 200
    loaded_response3 = json.loads(response3.data)
    if loaded_response3.get("status"):
        assert loaded_response3.get("status") == "Running"
    else:
        assert loaded_response3.get("message") == "Email received by user successfully"

def test_send_all_invitations(test_client, json_web_token):
    """Test send all invitations for an event endpoint
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_from_api = test_client.get('/v1/api/events/your_events', headers=headers)
    event = json.loads(event_from_api.data)['result'][0]
    event_id = event['id']
    response = test_client.post(f"/v1/api/invitations/send_all_invitations/{event_id}", headers=headers)
    assert response.status_code == 200
    loaded_response = json.loads(response.data)
    assert loaded_response.get("message") == "Emails sent successfully"

def test_rsvp(test_client, json_web_token):
    """Test RSVP feature
    """
    token, user = json_web_token
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get(f'/v1/api/invitations/invitations_sent', headers=headers)
    loaded_response = json.loads(response.data)
    assert response.status_code == 200
    assert len(loaded_response["result"]) == 2
    invitation1 = loaded_response["result"][0]
    invitation1_id = invitation1.get("id")
    invitation1_recipient_email = invitation1.get("recipient_email")
    invitation2 = loaded_response["result"][1]
    invitation2_id = invitation2.get("id")
    invitation2_recipient_email = invitation2.get("recipient_email")
    accept_data = {
        "status": "accepted"
    }
    reject_data = {
        "status": "rejected"
    }
    response2 = test_client.post(
        f'/v1/api/invitations/rsvp/{invitation1_id}/{invitation1_recipient_email}',
        data=json.dumps(accept_data),
        content_type='application/json',
        headers=headers
    )
    response3 = test_client.post(
        f'/v1/api/invitations/rsvp/{invitation2_id}/{invitation2_recipient_email}',
        data=json.dumps(reject_data),
        content_type='application/json',
        headers=headers
    )
    assert response2.status_code == 200
    assert response3.status_code == 200
    loaded_response2 = json.loads(response2.data)
    loaded_response3 = json.loads(response3.data)
    result1 = loaded_response2.get("result")
    result2 = loaded_response3.get("result")
    assert result1.get("status") == "accepted"
    assert result2.get("status") == "rejected"


def test_delete_invitation(test_client, json_web_token):
    """Test delete invitation endpoint
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/invitations/invitations_sent', headers=headers)
    loaded_response = json.loads(response.data)
    assert response.status_code == 200
    assert len(loaded_response["result"]) == 2
    invitation1 = loaded_response["result"][0]
    invitation_id = invitation1["id"]
    response2 = test_client.delete(f'/v1/api/invitations/{invitation_id}', headers=headers)
    loaded_response2 = json.loads(response2.data)
    print(loaded_response2)
    assert response2.status_code == 200
    assert loaded_response2['message'] == 'Invitation deleted successfully'

