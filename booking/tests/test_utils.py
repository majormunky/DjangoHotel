import pytest
import datetime
from mixer.backend.django import mixer
from rooms import models as room_models
from booking import models
from booking import utils


@pytest.fixture
def booking_list():
    booking1 = mixer.blend(models.Booking)
    booking1.save()

    booking2 = mixer.blend(models.Booking)
    booking2.save()

    return models.Booking.objects.all()


@pytest.fixture
def room_list():
    room1 = mixer.blend(room_models.Room)
    room2 = mixer.blend(room_models.Room)
    return room_models.Room.objects.all()


@pytest.mark.django_db
def test_check_bookings_with_date_range(room_list):
    start_date = datetime.datetime.today().date()
    end_date = datetime.datetime.today().date()
    result = utils.check_bookings_with_date_range(start_date, end_date)
    assert result.count() == 2
