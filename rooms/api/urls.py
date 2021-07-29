from django.urls import path
from rooms.api import views
from rooms.api import serializers

urlpatterns = [
    path("floors/", views.ListFloors.as_view(), name="api-floor-list"),
    path("rooms/", views.RoomsForFloorAPIView.as_view(), name="api-rooms-for-floor"),
    path(
        "floors/generate-rooms/",
        views.GenerateRoomsForFloorAPIView.as_view(),
        name="api-generate-rooms",
    ),
]
