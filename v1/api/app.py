#!/usr/bin/env python3

from db.engine import init_db, storage
from models.user import User
from dotenv import load_dotenv
from flask import Flask, request, abort, make_response
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

# MODEL CREATION IN THE DB
with app.app_context():
    storage.create_all()

@app.route('/new_user', methods=['POST'], strict_slashes=False)
def register():
    """Register new user
    """
    try:
        new_user = User(
            first_name='Justin',
            last_name='Ebedi',
            password='cftyuijhghgjhji987t6r',
            email='justin@gmail.com',
            phoneNo='09166327158',
        )
        new_user.save_new()
    except Exception as e:
        print(f'Could not create user: {str(e)}')
    return make_response({'message': 'User created'}, 201)

@app.route('/get_user/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get a user by id
    """
    try:
        user = storage.get_object_by('User', id=user_id)
        return make_response({'message': str(user)}, 201)
    except Exception as e:
        print(f'Failed to get user from DB: {str(e)}')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
