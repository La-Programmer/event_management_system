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

def test_user_registration(test_client, db_instance):
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
        user = db_instance.get_object_by('User', email=data['email'])
        user.delete()

def test_user_auth(test_client, db_instance):
        """Test user authentication
        """
        data = {
                'first_name': 'Tester',
                'last_name': 'Userer',
                'password': '6789fhjk',
                'email': 'tester@gmail.com',
                'phoneNo': '0987654321'
        }
        credentials = {
                'password': '6789fhjk',
                'email': 'tester@gmail.com',
        }
        test_client.post('/v1/api/users/register', data=json.dumps(data), content_type='application/json')
        response = test_client.post('/v1/api/users/auth', data=json.dumps(credentials), content_type='application/json')
        assert response.status_code == 200
        assert json.loads(response.data)['message'] == 'User authenticated successfully'
        user = db_instance.get_object_by('User', email=data['email'])
        user.delete()

def test_get_all_users(test_client, db_instance, create_test_users):
      """Test get all users endpoint
      """
      response = test_client.get('/v1/api/users')
      loaded_response = json.loads(response.data)
      assert response.status_code == 200
      assert loaded_response['message'] == 'Users gotten successfully'
      assert len(loaded_response['users']) == 3

def test_get_user(test_client, db_instance, create_test_users):
        """Test get user endpoint
        """
        response = test_client.get('/v1/api/users/test2@gmail.com')
        loaded_response = json.loads(response.data)
        user_dict = loaded_response['user']
        assert response.status_code == 200
        assert loaded_response['message'] == 'User gotten successfully'
        assert user_dict['email'] == 'test2@gmail.com'
        assert user_dict['first_name'] == 'Test2'

def test_update_user(test_client, db_instance, create_test_users):
        """Test update user endpoint
        """
        response1 = test_client.get('/v1/api/users/test2@gmail.com')
        assert response1.status_code == 200
        loaded_response = json.loads(response1.data)
        user_id = loaded_response['user']['id']
        update_data = {'email': 'new_updated_email@gmail.com'}
        response2 = test_client.put(f'/v1/api/users/{user_id}', data=json.dumps(update_data), content_type='application/json')
        loaded_response2 = json.loads(response2.data)
        user = loaded_response['user']
        updated_user = loaded_response2['user']
        assert user['id'] == updated_user['id']
        assert user['email'] != updated_user['email']
