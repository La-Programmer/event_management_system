#!/usr/bin/env python3
import json
import pytest
from sqlalchemy.exc import IntegrityError

@pytest.fixture(scope="module")
def test_client(flask_app):
        """Create flask test client
        """
        with flask_app.test_client() as client:
                yield client

def test_user_registration(test_client):
        """Test user registration
        """
        data = {
                'first_name': 'Test',
                'last_name': 'User',
                'password': '6789oigfhjk',
                'email': 'test@gmail.com',
                'phoneNo': '0987654321'
        }
        response = test_client.post('/v1/api/users/register', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'User registered successfully'

def test_user_auth(test_client):
        """Test user authentication
        """
        data = {
                'first_name': 'Test2',
                'last_name': 'User2',
                'password': '6789oigfhjk',
                'email': 'test2@gmail.com',
                'phoneNo': '0987654321'
        }
        credentials = {
                'password': '6789oigfhjk',
                'email': 'test2@gmail.com',
        }
        test_client.post('/v1/api/users/register', data=json.dumps(data), content_type='application/json')
        response = test_client.post('/v1/api/users/auth', data=json.dumps(credentials), content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'User authenticated successfully'
