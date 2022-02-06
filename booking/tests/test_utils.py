import pytest
import datetime
from booking import utils


@pytest.mark.django_db
def test_check_bookings_with_date_range_with_some_results(booking_list):
    start_date = datetime.date(2021, 8, 12)
    end_date = datetime.date(2021, 8, 16)
    result = utils.check_bookings_with_date_range(start_date, end_date)
    assert len(result) == 2


@pytest.mark.django_db
def test_checking_bookings_with_date_range_no_overlap(booking_list):
    start_date = datetime.date(2021, 10, 12)
    end_date = datetime.date(2021, 10, 16)
    result = utils.check_bookings_with_date_range(start_date, end_date)
    assert len(result) == 3
