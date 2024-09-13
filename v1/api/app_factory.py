#!/usr/bin/env python3

from ..db.engine import init_db, storage
from .app_config import DevConfig, TestConfig
from .views import app_views
from v1.api.celery_config import celery_init_app
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
import os

load_dotenv()

# ENV VARIABLES
env = os.environ.get('ENV')
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
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

    # CORS SETTING
    cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    
    # INTEGRATE WITH SWAGGER FOR DOCUMENTATION
    SWAGGER_URL="/swagger"
    API_URL="/static/swagger.json"
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Access API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # INTEGRATE WITH CELERY
    celery_init_app(app)

    # INTEGRATE WITH FLASK MAIL
    mail = Mail(app)
    app.mail = mail

    # MODEL CREATION IN THE DB
    with app.app_context():
        storage.create_all()
    return app
