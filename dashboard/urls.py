from django.urls import path
from dashboard import views


urlpatterns = [
	path("", views.index, name="dashboard-index"),
	path("floor-setup/", views.floor_setup, name="dashboard-floor-setup"),
]
