from django.urls import path
from . import views


urlpatterns = [
    path("book-room/", views.book_room, name="book-room"),
    path("ajax-check-booking/", views.ajax_check_booking, name="ajax-check-booking"),
]
