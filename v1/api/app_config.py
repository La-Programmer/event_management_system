#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# ENV VARIABLES
secret = os.environ.get('SECRET')
mail_server = os.environ.get('MAIL_SERVER')
mail_port = os.environ.get('MAIL_PORT')
mail_username = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')
REDIS = os.environ.get('REDIS')

class Config:
    CELERY = {
        "broker_url": REDIS,
        "result_backend": REDIS,
        "task_ignore_result": True,
        "broker_connection_retry_on_startup": True
    }
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_PASSWORD = mail_password
    MAIL_PORT = mail_port
    MAIL_SERVER = mail_server
    MAIL_USERNAME = mail_username
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
