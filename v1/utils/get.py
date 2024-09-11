#1/usr/bin/env python3



def get_classes(obj_str):
    from ..models.user import User
    from ..models.events import Event
    from ..models.invitations import Invitation
    if obj_str == User or obj_str == Event or obj_str == Invitation:
        return obj_str
    classes = {
        'User': User,
        'Event': Event,
        'Invitation': Invitation
    }
    obj = classes.get(obj_str)
    if obj:
        return obj
    else:
        raise KeyError(f'{obj_str} class does not exist')