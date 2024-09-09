#!/usr/bin/env python3
import pytest
from v1.controllers import user
from sqlalchemy.orm.exc import NoResultFound

def test_get_all_users(flask_app, create_test_users):
    with flask_app.app_context():
        try:
            users = user.get_all_users()
            assert len(users) == 5
        except Exception as e:
            pytest.fail(str(e))

def test_get_user_by(flask_app, create_test_users):
    with flask_app.app_context():
        try:
            user1 = user.get_user_by(email='test1@gmail.com')
            user2 = user.get_user_by(email='test2@gmail.com')
            user3 = user.get_user_by(email='test3@gmail.com')
            user4 = user.get_user_by(email='test4@gmail.com')
            assert user1.first_name == 'Test1'
            assert user2.first_name == 'Test2'
            assert user3.first_name == 'Test3'
            assert user4.first_name == 'Test4'
        except Exception as e:
            pytest.fail(str(e))

def test_update_user(flask_app, create_test_users):
    with flask_app.app_context():
        try:
            user1 = user.get_user_by(id=create_test_users[0].id)
            assert user1.email == 'test1@gmail.com'
            updated_user = user.update_user(user1.id, {'email': 'update_test@gmail.com'})
            updated_user_db = user.get_user_by(id=create_test_users[0].id)
            assert updated_user.email == updated_user_db.email
            assert user1.id == updated_user_db.id
            assert updated_user.id == updated_user_db.id
            with pytest.raises(NoResultFound):
                no_user = user.get_user_by(email='test1@gmail.com')
        except Exception as e:
            pytest.fail(str(e))

def test_delete_user(flask_app, create_test_users):
    with flask_app.app_context():
        try:
            user_id1 = create_test_users[3].id
            user_id2 = create_test_users[2].id
            user.delete_user(user_id1)
            user.delete_user(user_id2)
            with pytest.raises(NoResultFound):
                user1 = user.get_user_by(id=user_id1)
                user2 = user.get_user_by(id=user_id2)
        except Exception as e:
            pytest.fail(str(e))
