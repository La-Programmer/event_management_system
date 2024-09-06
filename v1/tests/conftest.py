#!/usr/bin/env python3

from v1.db.engine import storage
from v1.api.app_factory import create_app
from v1.api.app_config import TestConfig
from v1.models.user import User
from v1.controllers.auth import Auth
import pytest

app = create_app(TestConfig)

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

# @pytest.fixture
# def user_initialized_instance(request, scope="session"):
#     """Create an initialized test user instance
#     """
#     with app.app_context():
#         try:
#             new_user = User({
#                 'first_name': 'Test',
#                 'last_name': 'User',
#                 'password': '6789oigfhjk',
#                 'email': 'test@gmail.com',
#                 'phoneNo': '0987654321'
#             })
#             new_user.save_new()
#             yield new_user
#             new_user.delete()
#         except Exception as e:
#             pytest.fail(str(e))



@pytest.fixture(scope="session")
def auth_controller_instance(request):
    """Create an instance of the Auth controller
    """
    auth = Auth()
    yield auth
