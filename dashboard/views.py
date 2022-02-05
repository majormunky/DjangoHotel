import datetime
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.urls import reverse
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
            params = urlencode(
                {
                    "user": form.cleaned_data["user"].id,
                    "start_date": form.cleaned_data["start_date"].strftime("%m-%d-%Y"),
                    "end_date": form.cleaned_data["end_date"].strftime("%m-%d-%Y"),
                }
            )
            base_url = reverse("dashboard-find-room")
            url = "{}?{}".format(base_url, params)
            return redirect(url)
    else:
        form = booking_forms.BookingForm()
    return render(request, "dashboard/create-booking.html", {"form": form})


def find_room_for_booking(request):
    sd_from_url = request.GET.get("start_date", None)
    ed_from_url = request.GET.get("end_date", None)

    if sd_from_url is None or ed_from_url is None:
        return redirect("dashboard-create-booking")

    today = datetime.datetime.today()
    start_date = datetime.datetime.strptime(sd_from_url, "%m-%d-%Y")

    date_list = generate_date_list(start_date, 14)
    next_week = date_list[6]
    prev_week = start_date - datetime.timedelta(days=7)

    room_list = floor_models.Room.objects.all()

    # build up the room schedule
    room_schedule = {}

    for d in date_list:
        date_key = d.strftime("%m-%d-%Y")
        room_schedule[date_key] = []
        scheduled_room_list = floor_models.Room.objects.filter(
            scheduled_booking__start_date__lte=d, scheduled_booking__end_date__gte=d
        )
        if scheduled_room_list.exists():
            for s_room in scheduled_room_list:
                room_schedule[date_key].append(s_room)

    return render(
        request,
        "dashboard/find-room.html",
        {
            "room_list": room_list,
            "date_list": date_list,
            "today": today,
            "prev_week": prev_week,
            "next_week": next_week,
            "room_schedule": room_schedule,
        },
    )
