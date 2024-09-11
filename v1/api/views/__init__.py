#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/v1/api/')

from .users import *
from .events import *
from .invitations import *
