#!/usr/bin/env python3
import pytest
from sqlalchemy.exc import IntegrityError
from v1.api.app import app

def test_db_connection(db_instance):
    """Test that db is running
    """
    assert db_instance.is_alive() == True

# @pytest.mark.parametrize('user_instance', [{'first_name': 'Justin', 'last_name': 'The Great', 'password': '6789oigfhjk', 'email': 'justin@gmail.com', 'phoneNo': '0987654321'}], indirect=True)
def test_wrong_user_creation(user_instance):
    """Test that wrong user creation raises exception
    """
    user = user_instance(
        first_name='Test',
        last_name='User',
        password='6789oigfhjk',
        email='justin@gmail.com',
        phoneNo='0987654321')
    
    with pytest.raises(IntegrityError):
        with app.app_context():
            user.save_new()
    

# @pytest.mark.parametrize('user_instance', [{'first_name': 'Test', 'last_name': 'User', 'password': '6789oigfhjk', 'email': 'test@gmail.com', 'phoneNo': '0987654321'}], indirect=True)
# def test_user_creation(db_instance, user_instance):
#     """Test that user is successfully created in DB
#     """
#     saved_user = db_instance.get_object_by('User', email=user_instance.email)
#     assert user_instance.__dict__['id'] == saved_user.id

def test_create_user(db_instance, user_instance):
    """Test that user is successfully created in DB
    """
    user = user_instance(
        first_name='Test',
        last_name='User',
        password='6789oigfhjk',
        email='test@gmail.com',
        phoneNo='0987654321')
    
    try:
        user_dict = user.to_dict()
        user.save_new()
        saved_user = db_instance.get_object_by('User', email=user_instance.email)
        assert user_dict.get('id') == saved_user.id
    except Exception as e:
        pytest.fail(str(e))
    finally:
        user.delete()

def test_update_user(db_instance, user_instance):
    """Test that a user is updated successfully in DB
    """
    user = user_instance(
        first_name='Test',
        last_name='User',
        password='6789oigfhjk',
        email='test@gmail.com',
        phoneNo='0987654321')
    try:
        user_dict = user.to_dict()
        user.save_new()
        saved_user = db_instance.get_object_by('User', id=user.id)
        assert user_dict.get('id') == saved_user.id
        new_email = 'test2@gmail.com'
        saved_user.update(email=new_email)
        saved_user2 = db_instance.get_object_by('User', id=user.id)
        assert user_dict.get('email') != saved_user2.email
        assert new_email == saved_user2.email
    except Exception as e:
        pytest.fail(str(e))
    finally:
        user.delete()
