#!/usr/bin/env python3
import json

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

def test_delete_invitation(test_client, json_web_token, create_test_users):
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
