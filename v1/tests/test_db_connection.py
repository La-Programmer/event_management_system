#!/usr/bin/env python3

from v1.db.engine import storage

def test_db_connection():
    """Test that db is running
    """
    assert storage.is_alive() == True
