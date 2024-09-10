#!/usr/bin/env python3
import json
import pytest
# from sqlalchemy.exc import IntegrityError

def test_get_event_endpoint_without_login(test_client):
    """Test getting an event without logging in
    """
    response = test_client.get('/v1/api/events/12345678')
    assert response.status_code == 401
    assert json.loads(response.data)['msg'] == 'Missing Authorization Header'

def test_get_event_endpoint(test_client, json_web_token):
    """Test getting an event
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get('/v1/api/events/your_events', headers=headers)
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data['message'] == 'No events were found for this user'

def test_create_event_endpoint(test_client, json_web_token):
    """Test creating an event
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_data = {
        'event_owner': user['id'],
        'event_name': 'House Party',
        'event_location': '111 road, 3rd avenue, Gwarinpa',
        'date_time': '2023-08-26T16:00:00.0000'
    }
    response = test_client.post(
        '/v1/api/events/',
        data=json.dumps(event_data),
        headers=headers,
        content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Event created successfully'

def test_create_event_endpoint_unauthorized(test_client, json_web_token):
    """Test creating event without authorization
    """
    token, user = json_web_token
    event_data = {
        'event_owner': user['id'],
        'event_name': 'House Party',
        'event_location': '111 road, 3rd avenue, Gwarinpa',
        'date_time': '2023-08-26T16:00:00.0000'
    }
    response = test_client.post(
        '/v1/api/events/',
        data=json.dumps(event_data),
        content_type="application/json")
    assert response.status_code == 401
    assert json.loads(response.data)['msg'] == 'Missing Authorization Header'

def test_update_event_endpoint(test_client, json_web_token):
    """Test updating an event
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_from_api = test_client.get('/v1/api/events/your_events', headers=headers)
    event = json.loads(event_from_api.data)['result'][0]
    event_id = event['id']
    event_data = {
        'event_name': 'Updated event',
        'event_location': 'Updated location'
    }
    response = test_client.put(
        f'/v1/api/events/{event_id}',
        data=json.dumps(event_data),
        content_type="application/json",
        headers=headers)
    print(response.data)
    assert response.status_code == 200
    response_data = json.loads(response.data)['result']
    assert response_data.get('event_owner') == user.get('id')
    assert response_data.get('event_name') != event['event_name']
    assert response_data.get('event_location') != event['event_location']

def test_delete_event_endpoint(test_client, json_web_token):
    """Test deleting an event
    """
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    event_from_api = test_client.get('/v1/api/events/your_events', headers=headers)
    event = json.loads(event_from_api.data)['result'][0]
    event_id = event['id']
    response = test_client.delete(
        f'/v1/api/events/{event_id}',
        headers=headers
    )
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data.get('message') == 'Event deleted successfully'
    response2 = test_client.get(
        f'/v1/api/events/{event_id}',
        headers=headers
    )
    assert response2.status_code == 404
    response2_data = json.loads(response2.data)
    assert response2_data.get('message') == 'No event was found'
