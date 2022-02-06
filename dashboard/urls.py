from django.urls import path
from dashboard import views


urlpatterns = [
    path("dashboard/", views.index, name="dashboard-index"),
    path("dashboard/setup/", views.setup, name="dashboard-setup"),
    path("dashboard/bookings/", views.bookings_list, name="dashboard-booking"),
    path(
        "dashboard/bookings/<int:pk>/",
        views.booking_detail,
        name="dashboard-booking-detail",
    ),
    path(
        "dashboard/booking/create/",
        views.create_booking,
        name="dashboard-create-booking",
    ),
    path(
        "dashboard/booking/find-room/",
        views.find_room_for_booking,
        name="dashboard-find-room",
    ),
    path(
        "dashboard/ajax/book-room/",
        views.ajax_book_room,
        name="dashboard-ajax-book-room",
    ),
]
