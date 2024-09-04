#!/usr/bin/python3
"""
Instantiate DB class
"""
from ..db.engine import DB

storage = DB()
storage.reload()
