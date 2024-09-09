#!/usr/bin/env python3

from v1.db.engine import storage
from v1.models.user import User
from v1.utils.validate import validate_data

def get_all_users():
    """Get all users from the DB
    """
    try:
        users = storage.get_all('User')
        user_dict_array = [user.to_dict() for user in users]
        return user_dict_array
    except Exception:
        raise

def get_user_by(**kwargs) -> User:
    """Get a user by a specific keyword argument
    """
    try:
        user: User = storage.get_object_by('User', **kwargs)
        if user is None:
            return None
        return user
    except Exception:
        raise

def update_user(user_id, user_data) -> User:
    """Updates a user by ID
    """
    valid_keys = ['first_name', 'last_name', 'email', 'password', 'phoneNo']
    if validate_data(valid_keys, user_data):
        try:
            user: User = get_user_by(id=user_id)
            if user is None:
                return None
            user.update(**user_data)
            updated_user: User = get_user_by(id=user_id) 
            return updated_user
        except Exception as e:
            raise

def delete_user(user_id):
    """Deletes a user by ID
    """
    try:
        user = get_user_by(id=user_id)
        if user is None:
            raise Exception('User not found')
        user.delete()
    except Exception:
        raise
