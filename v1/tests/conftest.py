#!/usr/bin/env python3

from v1.db.engine import storage
from v1.api.app_factory import create_app
from v1.api.app_config import TestConfig
from v1.models.events import Event 
from v1.models.user import User
from v1.controllers.auth import Auth
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
    ]
    with flask_app.app_context():
        try:
            users = []
            for user in test_users:
                users.append(auth_controller_instance.register_user(user))
            yield users
        except Exception as e:
            pytest.fail(str(e))
