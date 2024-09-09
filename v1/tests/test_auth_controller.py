#!/usr/bin/env python3
import pytest

def test_user_registration(flask_app, auth_controller_instance, db_instance):
    """Test that a user is correctly registered
    """
    with flask_app.app_context():
        try:
            user = auth_controller_instance.register_user({
                'first_name': 'Test',
                'last_name': 'User',
                'password': '6789oigfhjk',
                'email': 'test@gmail.com',
                'phoneNo': '0987654321'
            })
            saved_user = db_instance.get_object_by('User', email=user.email)
            assert user.id == saved_user.id
        except Exception as e:
            pytest.fail(str(e))
        finally:
            user.delete()

def test_token_creation(flask_app, auth_controller_instance):
    """Test that a JWT token is correctly generated
    """
    with flask_app.app_context():
        try:
            user = auth_controller_instance.register_user({
                'first_name': 'Test',
                'last_name': 'User',
                'password': '6789oigfhjk',
                'email': 'test@gmail.com',
                'phoneNo': '0987654321'
            })
            print(user.id)
            try:
                token = auth_controller_instance.create_token(user.id)
                if token is None:
                    pytest.fail("Token generator function returned 'None'")
            except Exception as e:
                raise
        except Exception as e:
            pytest.fail(str(e))
        finally:
            user.delete()

def test_user_authentication(flask_app, auth_controller_instance):
    """Test that a user is authenticated corrected
    """
    with flask_app.app_context():
        try:
            user = auth_controller_instance.register_user({
                'first_name': 'Test',
                'last_name': 'User',
                'password': '6789oigfhjk',
                'email': 'test@gmail.com',
                'phoneNo': '0987654321'
            })
            try:
                authenticated_user = auth_controller_instance.authenticate({
                    'email': user.email,
                    'password': user.password
                })
                assert authenticated_user is not None
            except Exception as e:
                raise
        except Exception as e:
            pytest.fail(str(e))
        finally:
            user.delete()