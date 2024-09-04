#1/usr/bin/env python3



def get_classes(obj_str):
    from models.user import User
    classes = {
        'User': User,
        # 'Event': Event,
        # 'Invitation': Invitation
    }
    obj = classes[obj_str]
    return obj