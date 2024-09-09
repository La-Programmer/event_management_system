#!/usr/bin/env python3

def validate_data(valid_keys, user_data: dict) -> bool:
    """Validate the data sent to register a new user
    """
    received_keys = user_data.keys()
    for key in received_keys:
        if key not in valid_keys:
            return False
    return True        