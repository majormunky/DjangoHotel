from django.urls import path
from . import views


urlpatterns = [
    path("book-room/", views.book_room, name="book-room"),
]
