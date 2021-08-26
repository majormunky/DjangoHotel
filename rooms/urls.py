from django.urls import path, include
from . import views


urlpatterns = [
	path('dashboard/ajax/create-floor/', views.ajax_create_floor, name='rooms-ajax-create-floor'),
	path('dashboard/ajax/create-room/', views.ajax_create_room, name='rooms-ajax-create-room'),
	path('rooms/api/', include('rooms.api.urls')),
]
