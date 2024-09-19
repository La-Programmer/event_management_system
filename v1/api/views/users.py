#!/usr/bin/env python3
"""User model API endpoints
"""
from flask import request, make_response
from flask_jwt_extended import jwt_required
from ...controllers.auth import Auth, UserNotFound
from ...controllers import user
from . import app_views
from v1.db.engine import storage


auth = Auth()

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_all_users():
    """Get all users from DB
    """
    try:
        users = user.get_all_users()
        return make_response({'message': 'Users gotten successfully', 'result': users}, 200)
    except Exception as e:
        return make_response({'message': 'Error getting users', 'exception': str(e)}, 500)

@app_views.route('/users/<user_email>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_email):
    """Get a user by email
    """
    try:
        received_user = user.get_user_by(email=user_email)
        if received_user is None:
            return make_response({'message': 'User not found'}, 404)
        result = received_user.to_dict()
        return make_response({'message': 'User gotten successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Error getting user', 'exception': str(e)}, 500)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user(user_id):
    """Updates a user by ID
    """
    update_data = request.get_json()
    try:
        updated_user = user.update_user(user_id, update_data)
        if updated_user is None:
            return make_response({'message': 'User not found'}, 404)
        result = updated_user.to_dict()
        return make_response({'message': 'User updated successfully', 'result': result}, 200)
    except Exception as e:
        return make_response({'message': 'Error updating user', 'exception': str(e)}, 500)

@app_views.route('/users/register', methods=['POST'], strict_slashes=False)
def register_user():
    """Register a new user
    """
    user_data = request.get_json()
    try:
        # Check if the user already exists
        try:
            user = storage.get_object_by('User', email=user_data.get('email'))
            return make_response({'message': 'User already exists'}, 400)
        except Exception:
            new_user = auth.register_user(user_data)
            if new_user is None:
                return make_response({'message': 'Failed to register user controller returned "None"'}, 500)
            return make_response({'message': 'User registered successfully'}, 200)
    except Exception as e:
        return make_response({'message': 'Failed to create new user', 'exception': str(e)}, 500)

@app_views.route('/users/auth', methods=['POST'], strict_slashes=False)
def login():
    """Authenticate a user
    """
    user_data = request.get_json()
    try:
        user = auth.authenticate(user_data)
        if user:
            try:
                token = auth.create_token(user.get('id'))
                if token:
                    return make_response({'message': 'User authenticated successfully', 'result': user, 'token': token}, 200)
                return make_response({'message': 'Generated empty token'}, 500)
            except Exception as e:
                return make_response({'message': f'Auth token could not be generated', 'exception': str(e)}, 500)
        return make_response({'message': 'User not found'}, 404)
    except UserNotFound as e:
        return make_response({'message': 'User not found'}, 404)
    except Exception as e:
        return make_response({'message': f'User authentication failed', 'exception': str(e)}, 500)

# ADMIN ENDPOINT
### ADD DELETE USER ENDPOINT
