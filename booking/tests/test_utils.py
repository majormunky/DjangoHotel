import pytest
import datetime
from booking import utils


@pytest.mark.django_db
def test_check_bookings_with_date_range_with_some_results(booking_list):
    start_date = datetime.datetime(2021, 8, 12).date()
    end_date = datetime.datetime(2021, 8, 16).date()
    result = utils.check_bookings_with_date_range(start_date, end_date)
    assert len(result) == 2


@pytest.mark.django_db
def test_checking_bookings_with_date_range_no_overlap(booking_list):
    start_date = datetime.datetime(2021, 10, 12).date()
    end_date = datetime.datetime(2021, 10, 16).date()
    result = utils.check_bookings_with_date_range(start_date, end_date)
    print(result[0])
    assert len(result) == 3
