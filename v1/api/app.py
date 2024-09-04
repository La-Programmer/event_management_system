#!/usr/bin/env python3

from db.engine import init_db, storage
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
import os

load_dotenv()

# ENV VARIABLES FOR DB CONNECTION
user = os.environ.get('USER')
pwd = os.environ.get('PASS')
host = os.environ.get('HOST')
env = os.environ.get('ENV')
db = os.environ.get('DB')

# FLASK APP DEFINITION
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{user}:{pwd}@{host}/{db}"

# INITIALIZE DB WITH APP
print("Initializing DB....")
init_db(app)

# SETUP MIGRATIONS
migrate = Migrate(app, storage)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
