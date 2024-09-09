#!/usr/bin/python3
"""
Test file
"""

from models.base import BaseModel

new_user = BaseModel(
    first_name='Justin',
    last_name='Ebedi',
    password='cftyuijhghgjhji987t6r',
    email='justin@gmail.com',
    phoneNo='09166327158',)
print('---------NEW USER CREATED SUCCESSFULLY-----------')
print(new_user.to_dict())

