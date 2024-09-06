#!/usr/bin/env python3
"""User model API endpoints
"""
from flask import request, make_response
from flask_jwt_extended import jwt_required
from ...controllers.auth import Auth, UserNotFound
from . import app_views

auth = Auth()

@app_views.route('/users/register', methods=['POST'], strict_slashes=False)
def register_user():
    """Register a new user
    """
    user_data = request.get_json()
    try:
        new_user = auth.register_user(user_data)
        if new_user is None:
            return make_response({'message': f'Failed to register user controller returned "None"'}, 500)
        return make_response({'message': 'User registered successfully'}, 200)
    except Exception as e:
        return make_response({'message': f'Failed to create new user', 'exception': str(e)}, 500)

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
                    return make_response({'message': 'User authenticated successfully', 'user': user, 'token': token}, 200)
                return make_response({'message': 'Generated empty token'}, 500)
            except Exception as e:
                return make_response({'message': f'Auth token could not be generated', 'exception': str(e)}, 500)
    except UserNotFound as e:
        return make_response({'message': 'User not found'}, 404)
    except Exception as e:
        return make_response({'message': f'User authentication failed', 'exception': str(e)}, 500)
