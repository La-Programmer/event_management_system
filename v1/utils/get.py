#1/usr/bin/env python3



def get_classes(obj_str):
    from ..models.user import User
    if obj_str == User:
        return obj_str
    classes = {
        'User': User,
        # 'Event': Event,
        # 'Invitation': Invitation
    }
    obj = classes.get(obj_str)
    if obj:
        return obj
    else:
        raise KeyError(f'{obj_str} class does not exist')