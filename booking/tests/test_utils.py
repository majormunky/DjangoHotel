import pytest
import datetime
import pytz
from mixer.backend.django import mixer
from rooms import models as room_models
from booking import models
from booking import utils


@pytest.fixture
def booking_list():
    tz = pytz.timezone("US/Pacific")
    b1_start_date = datetime.datetime(2021, 8, 1, 17, 0, 0).astimezone(tz)
    b1_end_date = datetime.datetime(2021, 8, 10, 11, 0, 0).astimezone(tz)
    room1 = mixer.blend(room_models.Room)
    room1.save()
    booking1 = mixer.blend(
        models.Booking,
        start_date=b1_start_date,
        end_date=b1_end_date,
        scheduled_room=room1,
    )
    booking1.save()

    b2_start_date = datetime.datetime(2021, 8, 4, 17, 0, 0).astimezone(tz)
    b2_end_date = datetime.datetime(2021, 8, 15, 11, 0, 0).astimezone(tz)
    room2 = mixer.blend(room_models.Room)
    room2.save()
    booking2 = mixer.blend(
        models.Booking,
        start_date=b2_start_date,
        end_date=b2_end_date,
        scheduled_room=room2,
    )
    booking2.save()

    room3 = mixer.blend(room_models.Room)
    room3.save()

    return models.Booking.objects.all()


@pytest.mark.django_db
def test_check_bookings_with_date_range(booking_list):
    start_date = datetime.datetime(2021, 8, 12).date()
    end_date = datetime.datetime(2021, 8, 16).date()
    result = utils.check_bookings_with_date_range(start_date, end_date)
    assert len(result) == 2
