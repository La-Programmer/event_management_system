#!/usr/bin/env python3
import json
import pytest
from sqlalchemy.exc import IntegrityError

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

def test_get_all_users(test_client, json_web_token):
      """Test get all users endpoint
      """
      token, user = json_web_token
      headers = {'Authorization': f'Bearer {token}'}
      response = test_client.get('/v1/api/users', headers=headers)
      loaded_response = json.loads(response.data)
      assert response.status_code == 200
      assert loaded_response['message'] == 'Users gotten successfully'
      assert len(loaded_response['result']) == 4

def test_get_user(test_client, json_web_token):
        """Test get user endpoint
        """
        token, user = json_web_token
        print(token)
        headers = {'Authorization': f'Bearer {token}'}
        response = test_client.get('/v1/api/users/test2@gmail.com', headers=headers)
        loaded_response = json.loads(response.data)
        user_dict = loaded_response['result']
        assert response.status_code == 200
        assert loaded_response['message'] == 'User gotten successfully'
        assert user_dict['email'] == 'test2@gmail.com'
        assert user_dict['first_name'] == 'Test2'

def test_get_user_without_login(test_client):
        """Test get user endpoint
        """
        response = test_client.get('/v1/api/users/test2@gmail.com')
        loaded_response = json.loads(response.data)
        assert response.status_code == 401
        assert loaded_response['msg'] == 'Missing Authorization Header'

def test_update_user(test_client, json_web_token):
        """Test update user endpoint
        """
        token, user = json_web_token
        headers = {'Authorization': f'Bearer {token}'}
        response1 = test_client.get('/v1/api/users/test2@gmail.com', headers=headers)
        assert response1.status_code == 200
        loaded_response = json.loads(response1.data)
        user_id = loaded_response['result']['id']
        update_data = {'email': 'new_updated_email@gmail.com'}
        headers = {'Authorization': f'Bearer {token}'}
        response2 = test_client.put(
                f'/v1/api/users/{user_id}',
                data=json.dumps(update_data),
                content_type='application/json',
                headers=headers
        )
        loaded_response2 = json.loads(response2.data)
        user = loaded_response['result']
        updated_user = loaded_response2['result']
        assert user['id'] == updated_user['id']
        assert user['email'] != updated_user['email']
