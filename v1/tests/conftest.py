#!/usr/bin/env python3

from v1.db.engine import storage
from v1.api.app import app
from v1.models.user import User
import pytest

@pytest.fixture
def db_instance(scope="session"):
    """Create a test DB instance
    """
    with app.app_context(): 
        yield storage
        storage.close()

@pytest.fixture
def user_instance(request, scope="session"):
    """Create a test user instance
    """
    # user_args = request.param if hasattr(request, 'param') else {}
    # new_user = User(**user_args)
    # with app.app_context():
    #     try:
    #             new_user.save_new()
    #     except IntegrityError as e:
    #         pytest.fail(f"IntegrityError occurred: {e}")
    #     yield new_user
    #     new_user.delete()
    new_user = User
    yield new_user
    
