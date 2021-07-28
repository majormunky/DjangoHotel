from django.urls import path
from dashboard import views


urlpatterns = [
    path("dashboard/", views.index, name="dashboard-index"),
    path("dashboard/setup/", views.setup, name="dashboard-setup"),
]
