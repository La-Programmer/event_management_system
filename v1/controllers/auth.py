#!/usr/bin/env python3

from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from models.user import User
from db.engine import storage

# CUSTOM AUTHENTICATION BASED EXCEPTION
class UserNotFound(Exception):
    """User not found exception"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
    
    def __str__(self):
        return f"Authenticaton Failed: {self.message}"


class JWTAuth:
    """Handles JWT Authentication
    """
