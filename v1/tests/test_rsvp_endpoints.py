#!/usr/bin/env python3
import json
from v1.controllers import rsvp

def test_get_rsvp_data(test_client, json_web_token, test_invitations):
    """Test get rsvp data endpoint
    """
    invitation_id = test_invitations[3].id
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    response = test_client.get(f'/v1/api/rsvp/{invitation_id}', headers=headers)
    loaded_response = json.loads(response.data)
    assert response.status_code == 200
    response_result = loaded_response["result"]
    expected_keys = ["recipient_name", "event_name", "message"]
    received_keys = response_result.keys()
    for key in expected_keys:
        assert key in received_keys

def test_rsvp_to_iv(test_client, json_web_token, test_invitations):
    """Test RSVP to invitation endpoint
    """
    invitation_id = test_invitations[3].id
    invitation2_id = test_invitations[4].id
    token, user = json_web_token
    headers = {'Authorization': f'Bearer {token}'}
    data = {"status": "true"}
    data2 = {"status": "false"}
    response = test_client.post(f'/v1/api/rsvp/{invitation_id}', data=json.dumps(data), headers=headers, content_type='application/json')
    response2 = test_client.post(f'/v1/api/rsvp/{invitation2_id}', data=json.dumps(data2), headers=headers, content_type='application/json')
    print(response.data)
    print(response2.data)
    assert response.status_code == 200
    assert response2.status_code == 200
    
