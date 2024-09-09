#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# ENV VARIABLES
secret = os.environ.get('SECRET')

class Config:
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_SECRET_KEY = secret

class DevConfig(Config):
    user = os.environ.get('USER')
    pwd = os.environ.get('PASS')
    host = os.environ.get('HOST')
    env = os.environ.get('ENV')
    db = os.environ.get('DB')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}"


class TestConfig(Config):
    user = os.environ.get('USER')
    pwd = os.environ.get('PASS')
    host = os.environ.get('HOST')
    env = os.environ.get('ENV')
    db = os.environ.get('TEST_DB')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}"
    TESTING = True