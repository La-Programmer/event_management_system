#!/usr/bin/env python3

import pytest
from ..db import storage
from ..db.engine import DB

def test_db_connection():
    """Test that db is running
    """
    assert storage.is_alive() == True
