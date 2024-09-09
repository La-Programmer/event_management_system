#!/usr/bin/env python3

import pytest
from datetime import datetime
from v1.controllers import event
from v1.controllers.event import AccessDenied
from sqlalchemy.orm.exc import NoResultFound

time = "%Y-%m-%dT%H:%M:%S.%f"

@pytest.fixture(scope="module")
def test_events(create_test_users):
    """Create test events objects
    """
    owner_ids = [user.id for user in create_test_users]
    data = [
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday 2',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[0],
            'event_name': 'Mummy\'s birthday 3',
            'event_location': '31 road, 4th avenue, Oba-ile',
            'date_time': '2024-10-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[1],
            'event_name': 'Gloria\'s wedding',
            'event_location': '31 road, 5th avenue, Oba-ile',
            'date_time': '2024-11-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[2],
            'event_name': 'Convocatio Day',
            'event_location': '31 road, 6th avenue, Oba-ile',
            'date_time': '2024-12-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[3],
            'event_name': 'Babygirl\'s birthday',
            'event_location': '31 road, 7th avenue, Oba-ile',
            'date_time': '2024-09-26T16:00:00.0000'
        },
        {
            'event_owner': owner_ids[4],
            'event_name': 'Christmas Day',
            'event_location': '31 road, 8th avenue, Oba-ile',
            'date_time': '2024-08-26T16:00:00.0000'
        },
    ]
    test_events_list = []
    for event_data in data:
        new_event = event.create_event(event_data)
        test_events_list.append(new_event)
    yield test_events_list

def test_get_event(test_events):
    """Test getting an event
    """
    try:
        event1 = event.get_event(test_events[0].id)
        event2 = event.get_event(test_events[1].id)
        event3 = event.get_event(test_events[2].id)
        event4 = event.get_event(test_events[3].id)
        assert event1.id == test_events[0].id
        assert event1.event_name == test_events[0].event_name
        assert event1.event_owner == test_events[0].event_owner
        assert event1.date_time == test_events[0].date_time
        assert event2.id == test_events[1].id
        assert event2.event_name == test_events[1].event_name
        assert event2.event_owner == test_events[1].event_owner
        assert event2.date_time == test_events[1].date_time
        assert event3.id == test_events[2].id
        assert event3.event_name == test_events[2].event_name
        assert event3.event_owner == test_events[2].event_owner
        assert event3.date_time == test_events[2].date_time
        assert event4.id == test_events[3].id
        assert event4.event_name == test_events[3].event_name
        assert event4.event_owner == test_events[3].event_owner
        assert event4.date_time == test_events[3].date_time
    except Exception as e:
        pytest.faile(str(e))

def test_get_events_by_owner(test_events, create_test_users):
    """Test function that gets all the events of a user
    """
    try:
        owner_id = create_test_users[0].id
        events = event.get_events_by_owner(owner_id)
        assert len(events) == 3
        assert events[0].event_owner == events[1].event_owner
        assert events[1].event_owner == events[2].event_owner
        assert events[0].event_name != events[1].event_name
        assert events[1].event_name != events[2].event_name
    except Exception as e:
        pytest.fails(str(e))


def test_create_event(create_test_users):
    """Test event creation
    """
    owner = create_test_users[2]
    owner_id = owner.id
    data = {
        'event_owner': owner_id,
        'event_name': 'Mummy\'s birthday',
        'event_location': '31 road, 4th avenue, Oba-ile',
        'date_time': '2024-10-26T16:00:00.0000'
    }
    try:
        new_event = event.create_event(data)
        new_event_from_db = event.get_event(new_event.id)
        assert new_event.event_owner == owner_id
        assert new_event.event_owner == new_event_from_db.event_owner
        assert new_event.event_name == 'Mummy\'s birthday'
        assert new_event.event_name == new_event_from_db.event_name
        assert new_event.date_time == datetime.strptime(data['date_time'], time)
    except Exception as e:
        pytest.fail(str(e))

def test_update_event(test_events):
    """Test updating an event
    """
    event1 = test_events[0]
    assert event1.event_name == 'Mummy\'s birthday'
    owner_id = event1.event_owner
    event_id = event1.id
    try:
        updated_event = event.update_event(event_id, owner_id, {'event_name': 'Updated event name'})
        assert event1.event_name != 'Mummy\'s birthday'
        assert event1.event_name == 'Updated event name'
        assert event1.event_name == updated_event.event_name
        assert event1.id == updated_event.id
        assert event1.event_owner == updated_event.event_owner
    except Exception as e:
        pytest.fail(str(e))

def test_update_event_unauthorized(test_events):
    """Test updating an event as an unauthorized user
    """
    event2 = test_events[1]
    assert event2.event_name == 'Mummy\'s birthday 2'
    event_id = event2.id
    try:
        with pytest.raises(AccessDenied):
            updated_event = event.update_event(event_id, '4567890987dfghj', {'event_name': 'Updated event name'})
    except Exception as e:
        pytest.fail(str(e))

def test_delete_event(test_events):
    """Test deleting an event
    """
    event1 = test_events[0]
    event_id = event1.id
    owner_id = event1.event_owner
    try:
        event.delete_event(event_id, owner_id)
        with pytest.raises(NoResultFound):
            event.get_event(event_id)
    except Exception as e:
        pytest.fails(str(e))

def test_delete_event_unauthorized(test_events):
    """Test deleting an event as an unauthorized user
    """
    event2 = test_events[1]
    event_id = event2.id
    try:
        with pytest.raises(AccessDenied):
            event.delete_event(event_id, '67890-98798-iu88u')
    except Exception as e:
        pytest.fails(str(e))
