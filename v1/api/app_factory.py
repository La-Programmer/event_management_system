#!/usr/bin/env python3

from ..db.engine import init_db, storage
from .app_config import DevConfig, TestConfig
from .views import app_views
from v1.api.celery_config import celery_init_app
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os

load_dotenv()
env = os.environ.get('ENV')
if env == 'test':
    object = TestConfig
else:
    object = DevConfig
def create_app():
    app = Flask(__name__)
    app.config.from_object(object)

    # INITIALIZE FLASK APP
    init_db(app)
    JWTManager(app)
    app.register_blueprint(app_views)

    # SETUP MIGRATIONS
    migrate = Migrate(app, storage)

    # MODEL CREATION IN THE DB
    with app.app_context():
        storage.create_all()
    celery_init_app(app)
    return app
