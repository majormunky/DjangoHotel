from django.urls import path
from dashboard import views


urlpatterns = [
	path("", views.index, name="dashboard-index"),
	path("floor-setup/", views.floor_setup, name="dashboard-floor-setup"),
	path("floor-detail/<int:pk>/", views.floor_detail, name="dashboard-floor-detail"),
	path("room-detail/<int:pk>", views.room_detail, name="dashboard-room-detail"),
]
