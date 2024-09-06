#!/usr/bin/env python3

from ..db.engine import init_db, storage
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .views import app_views

def create_app(object):
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
    
    return app
