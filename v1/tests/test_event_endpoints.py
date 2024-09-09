#!/usr/bin/env python3
import json
import pytest
# from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope="module")
def test_client(flask_app):
    """Create flask test client
    """
    with flask_app.test_client() as client:
        yield client

def test_get_event_endpoint_without_login(test_client):
    """Test getting an event without logging in
    """
    response = test_client.get('/v1/api/events/12345678')
    print(response.data)
    assert response.status_code == 401
    assert json.loads(response.data)['msg'] == 'Missing Authorization Header'
