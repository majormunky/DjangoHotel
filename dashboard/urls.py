from django.urls import path
from dashboard import views


urlpatterns = [
    path("dashboard/", views.index, name="dashboard-index"),
    path("dashboard/setup/", views.setup, name="dashboard-setup"),
    path("dashboard/bookings/", views.bookings, name="dashboard-booking"),
    path(
        "dashboard/booking/create/",
        views.create_booking,
        name="dashboard-create-booking",
    ),
]
