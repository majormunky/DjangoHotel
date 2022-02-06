import json
import datetime
from urllib.parse import urlencode
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import get_user_model
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
            # figure out how many total days the person wants to stay
            # the date doesn't include the last day so we add 1 to our result
            total_days = (
                form.cleaned_data["end_date"] - form.cleaned_data["start_date"]
            ).days + 1

            params = urlencode(
                {
                    "user": form.cleaned_data["user"].id,
                    "start_date": form.cleaned_data["start_date"].strftime("%m-%d-%Y"),
                    "end_date": form.cleaned_data["end_date"].strftime("%m-%d-%Y"),
                    "total_days": total_days,
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
    user_id = request.GET.get("user", None)
    total_days = request.GET.get("total_days", None)

    if not all([sd_from_url, ed_from_url, user_id, total_days]):
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
            "user_id": user_id,
            "total_days": int(total_days),
        },
    )


def booking_detail(request, pk):
    booking_data = get_object_or_404(booking_models.Booking, pk=pk)
    return render(
        request, "dashboard/booking-detail.html", {"booking_data": booking_data}
    )


def ajax_book_room(request):
    user_id = request.POST.get("user_id", None)
    room_list = request.POST.get("rooms")
    room_list = json.loads(room_list)

    room_key = None
    room_days = []

    for room in room_list:
        if room_key is None:
            room_key = room["room_key"]

        date_obj = datetime.datetime.strptime(room["room_date"], "%m-%d-%Y").date()
        room_days.append(date_obj)

    room_days = sorted(room_days)
    start_date = room_days[0]
    end_date = room_days[-1]

    user_obj = get_object_or_404(get_user_model(), pk=user_id)

    room_parts = room_key.split(":")

    floor_obj = floor_models.Floor.objects.get(number=room_parts[0])

    print("Floor Obj:", floor_obj)
    room_num = room_parts[1]
    print("room num", room_num, "done room num")
    room_obj = floor_models.Room.objects.get(
        number=room_parts[1].strip(), floor=floor_obj
    )
    print(room_obj)

    new_booking = booking_models.Booking(
        start_date=start_date,
        end_date=end_date,
        user=user_obj,
        scheduled_room=room_obj,
    )
    new_booking.save()
    print(new_booking.id)

    new_url = reverse("dashboard-booking-detail", args=[new_booking.id])

    return JsonResponse({"result": "success", "redirect_url": new_url})
