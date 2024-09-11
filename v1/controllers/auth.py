#!/usr/bin/env python3

from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from v1.controllers.user import get_user_by
from v1.db.engine import storage
from v1.models.user import User
from v1.utils.validate import validate_data
import bcrypt


load_dotenv()
# CUSTOM AUTHENTICATION BASED EXCEPTION
class UserNotFound(Exception):
    """User not found exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"Authenticaton Failed: {self.message}"


class Auth:
    """Handles JWT Authentication
    """
    def __init__(self):
        self._db = storage

    def register_user(self, user_info: dict) -> User | None:
        """Register unregistered user"""
        try:
            valid_keys = ['first_name', 'last_name', 'email', 'password', 'phoneNo']
            if validate_data(valid_keys, user_info):
                new_user: User = User(**user_info)
                new_user.save_new()
                result = get_user_by(id=new_user.id)
                return result
            else:
                raise Exception('Missing key or invalid key in request')
        except Exception as e:
            raise
    
    def create_token(self, id: str) -> str | None:
        """Create access token for a user"""
        if id:
            try:
                token: str = create_access_token(identity=id)
                return token
            except Exception as e:
                raise
        else:
            return None
    
    # def construct_user_object(self, user_info: dict) -> dict | None:
    #     """Construct a user object"""
    #     if (user_info):
    #         user_object: dict = {
    #             'id'
    #             'email': user_info['email'],
    #             'first_name': user_info['first_name'],
    #             'last_name': user_info['last_name']
    #         }
    #         return user_object
    #     else:
    #         return None
    
    def authenticate(self, request_data) -> dict | None:
        """Handle all authentication logic
        """
        valid_keys = ['email', 'password']
        if validate_data(valid_keys, request_data):
            email = request_data['email']
            password = request_data['password']
            if email and password:
                try:
                    user: User = storage.get_object_by('User', email=email)
                    if user is None:
                        raise UserNotFound(f'User with email {email} not found')
                    password = password.encode('utf-8')
                    hashed_password = user.password.encode('utf-8')
                    verify_user: bool = bcrypt.checkpw(password, hashed_password)
                    if verify_user:
                        user_dict = user.to_dict()
                        return user_dict
                    return False
                except Exception as e:
                    raise
        else:
            raise Exception('Missing key or invalid key in request')
