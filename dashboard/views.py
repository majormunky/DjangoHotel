import datetime
from django.shortcuts import render, redirect
from rooms import models as floor_models
from booking import forms as booking_forms
from booking import models as booking_models

# TODO: Move to a utils file
def generate_date_list(start_date, days_to_generate):
    result = [start_date]
    day_delta = datetime.timedelta(hours=24)
    for i in range(days_to_generate):
        start_date += day_delta
        result.append(start_date)
    return result


def index(request):
    return render(request, "dashboard/index.html", {})


def setup(request):
    floor_list = floor_models.Floor.objects.all()
    return render(request, "dashboard/setup.html", {"floor_list": floor_list})


def bookings_list(request):
    bookings_list = booking_models.Booking.objects.all()
    return render(
        request, "dashboard/bookings-list.html", {"bookings_list": bookings_list}
    )


def create_booking(request):
    if request.method == "POST":
        form = booking_forms.BookingForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.is_active = False
            item.save()

            return redirect("dashboard-find-room", pk=item.id)
    else:
        form = booking_forms.BookingForm()
    return render(request, "dashboard/create-booking.html", {"form": form})


def find_room_for_booking(request, pk):
    start_date = datetime.datetime.today()
    date_list = generate_date_list(start_date, 14)

    room_list = floor_models.Room.objects.all()
    return render(
        request,
        "dashboard/find-room.html",
        {"room_list": room_list, "date_list": date_list},
    )
