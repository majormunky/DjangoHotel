from django.urls import path
from rooms.api import views
from rooms.api import serializers

urlpatterns = [
    path('floors/', views.ListFloors.as_view(), name='api-floor-list'),
]
