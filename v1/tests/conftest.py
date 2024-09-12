#!/usr/bin/env python3

from v1.api.app_factory import create_app
from v1.controllers import event 
from v1.controllers.auth import Auth
from v1.controllers import invitation
from v1.db.engine import storage
from v1.models.user import User
import json
import pytest
import os

os.environ['ENV'] = 'test'
app = create_app()

@pytest.fixture(scope="session")
def flask_app():
    """Create a flask app
    """
    yield app
    with app.app_context():
        storage.drop_all()

@pytest.fixture(scope="session")
def db_instance():
    """Create a test DB instance
    """ 
    with app.app_context():
        yield storage
        storage.close()

@pytest.fixture(scope="session")
def user_instance(request):
    """Create a test user instance
    """
    new_user = User
    yield new_user

@pytest.fixture(scope="session")
def auth_controller_instance(request):
    """Create an instance of the Auth controller
    """
    auth = Auth()
    yield auth

@pytest.fixture(scope="session")
def create_test_users(flask_app, auth_controller_instance):
    test_users = [
        {
            'first_name': 'Test1',
            'last_name': 'User1',
            'password': '6789oigfhjk',
            'email': 'test1@gmail.com',
            'phoneNo': '0987654321'
        },
        {
            'first_name': 'Test2',
            'last_name': 'User2',
            'password': '6789oigfhjk',
            'email': 'test2@gmail.com',
            'phoneNo': '0987654321'
        },
        {
            'first_name': 'Test3',
            'last_name': 'User3',
            'password': '6789oigfhjk',
            'email': 'test3@gmail.com',
            'phoneNo': '0987654321'
        },
        {
            'first_name': 'Test4',
            'last_name': 'User4',
            'password': '6789oigfhjk',
            'email': 'test4@gmail.com',
            'phoneNo': '0987654321'
        },
        {
            'first_name': 'Test5',
            'last_name': 'User5',
            'password': '6789oigfhjk',
            'email': 'test5@gmail.com',
            'phoneNo': '0987654321'
        },
        {
            'first_name': 'Invitation_sender',
            'last_name': 'Sender',
            'password': 'hu7uhhs&89wbu',
            'email': 'invitation@gmail.com',
            'phoneNo': '0908284617'
        }
    ]
    with flask_app.app_context():
        try:
            users = []
            for user in test_users:
                users.append(auth_controller_instance.register_user(user))
            yield users
        except Exception as e:
            pytest.fail(str(e))

@pytest.fixture(scope="session")
def test_events(create_test_users):
    """Create test events objects
    """
    owner_ids = [user.id for user in create_test_users]
    data = [
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday 2',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday 3',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[1],
            'event_name': 'Gloria\'s wedding',
            'event_location': '31 road, 5th avenue, Oba-ile',
            'date_time': '2024-11-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[2],
            'event_name': 'Convocatio Day',
            'event_location': '31 road, 6th avenue, Oba-ile',
            'date_time': '2024-12-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[3],
            'event_name': 'Babygirl\'s birthday',
            'event_location': '31 road, 7th avenue, Oba-ile',
            'date_time': '2024-09-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[4],
            'event_name': 'Christmas Day',
            'event_location': '31 road, 8th avenue, Oba-ile',
            'date_time': '2024-08-26T16:00:00.0000'
        },
    ]
    test_events_list = []
    for event_data in data:
        new_event = event.create_event(event_data)
        test_events_list.append(new_event)
    yield test_events_list

@pytest.fixture(scope="session")
def test_client(flask_app):
    """Create flask test client
    """
    with flask_app.test_client() as client:
        yield client

@pytest.fixture(scope="session")
def json_web_token(test_client):
    """Generate JWT for testing
    """
    data = {
            'first_name': 'Auth_tester',
            'last_name': 'Auth_userer',
            'password': 'auth_password',
            'email': 'auth_tester1@gmail.com',
            'phoneNo': '0987654321'
    }
    credentials = {
        'password': 'auth_password',
        'email': 'auth_tester1@gmail.com', 
    }
    try:
        test_client.post('/v1/api/users/register', data=json.dumps(data), content_type='application/json')
        response = test_client.post('/v1/api/users/auth', data=json.dumps(credentials), content_type='application/json')
        response_data = json.loads(response.data)
        print(response_data)
        assert response.status_code == 200
        token = response_data['token']
        user = response_data['result']
        yield token, user
        user = storage.get_object_by('User', email=data['email'])
        user.delete()
    except Exception as e:
        pytest.fail(str(e))

@pytest.fixture(scope="session")
def test_invitations(create_test_users, test_events, json_web_token):
    """Create test invitation objects
    """
    token, user = json_web_token
    user_fullname = user['first_name'] + ' ' + user['last_name']
    owner_ids = [user.id for user in create_test_users]
    event_ids = [event.id for event in test_events]
    print("Event IDs", event_ids)
    data = [
        {
            'recipient_id': owner_ids[0],
            'sender_id': owner_ids[len(owner_ids) - 1],
            'event_id': event_ids[0],
            'recipient_name': create_test_users[0].get_fullname(),
            'recipient_number': create_test_users[0].phoneNo,
            'recipient_email': create_test_users[0].email,
            'message': 'You are invited to my wedding',
        },
        {
            'recipient_id': owner_ids[1],
            'sender_id': owner_ids[len(owner_ids) - 1],
            'event_id': event_ids[0],
            'recipient_name': create_test_users[1].get_fullname(),
            'recipient_number': create_test_users[1].phoneNo,
            'recipient_email': create_test_users[1].email,
            'message': 'You are invited to my wedding',
        },
        {
            'recipient_id': owner_ids[2],
            'sender_id': owner_ids[len(owner_ids) - 1],
            'event_id': event_ids[4],
            'recipient_name': create_test_users[2].get_fullname(),
            'recipient_number': create_test_users[2].phoneNo,
            'recipient_email': create_test_users[2].email,
            'message': 'You are invited to my party',
        },
        {
            'recipient_id': owner_ids[3],
            'sender_id': owner_ids[len(owner_ids) - 1],
            'event_id': event_ids[5],
            'recipient_name': create_test_users[3].get_fullname(),
            'recipient_number': create_test_users[3].phoneNo,
            'recipient_email': create_test_users[3].email,
            'message': 'You are invited to my Christmas party',
        },
        {
            'recipient_id': user['id'],
            'sender_id': owner_ids[len(owner_ids) - 1],
            'event_id': event_ids[5],
            'recipient_name': user_fullname,
            'recipient_number': user['phoneNo'],
            'recipient_email': user['email'],
            'message': 'You are invited to my Christmas party',
        }
    ]
    test_invitations_list = []
    for invitation_data in data:
        new_invitations = invitation.create_invitation(invitation_data)
        test_invitations_list.append(new_invitations)
    yield test_invitations_list

@pytest.fixture(scope="session")
def test_event_for_iv(json_web_token):
    """Create an event for test invitation generation in testing IV endpoints
    """
    token, user = json_web_token
    event_data = {
        'event_owner': user['id'],
        'event_name': 'Evently product launch',
        'event_location': 'Transcorp, Abuja',
        'date_time': '2023-10-26T16:00:00.0000'   
    }
    try:
        new_event = event.create_event(event_data)
        return new_event
    except Exception as e:
        pytest.fail(str(e))
