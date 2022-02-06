import json
import pytest
from dashboard import utils


# booking_list test data has 2 bookings setup
# booking1 2021-8-1 -> 2021-8-10 room 1:1
# booking2 2021-8-4 -> 2021-8-15 room 1:2


@pytest.mark.django_db
def test_utils_book_room_works(normal_user, booking_list):

    post_data = {
        "rooms": '[{"room_key":"1: 3","room_date":"08-02-2021"},{"room_key":"1: 3","room_date":"08-03-2021"},{"room_key":"1: 3","room_date":"08-04-2021"}]',
        "user_id": normal_user.id,
    }

    room_data = json.loads(post_data["rooms"])

    result = utils.book_room(post_data["user_id"], room_data)
    assert result is not None


@pytest.mark.django_db
def test_utils_book_room_with_schedule_conflict(normal_user, booking_list):
    room_string = '[{"room_key":"1: 1","room_date":"08-02-2021"},{"room_key":"1: 1","room_date":"08-03-2021"},{"room_key":"1: 1","room_date":"08-04-2021"}]'
    room_data = json.loads(room_string)

    result = utils.book_room(normal_user.id, room_data)
    assert result is None


@pytest.mark.django_db
def test_utils_book_room_with_person_in_room(normal_user, booking_list_room1_occupied):
    room_string = '[{"room_key":"1: 1","room_date":"08-02-2021"},{"room_key":"1: 1","room_date":"08-03-2021"},{"room_key":"1: 1","room_date":"08-04-2021"}]'
    room_data = json.loads(room_string)

    result = utils.book_room(normal_user.id, room_data)
    assert result is None
