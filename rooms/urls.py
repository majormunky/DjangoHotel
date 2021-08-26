from django.urls import path, include
from . import views


urlpatterns = [
	path('ajax/create-floor/', views.ajax_create_floor, name='rooms-ajax-create-floor'),
	path('ajax/create-room/', views.ajax_create_room, name='rooms-ajax-create-room'),
	path("ajax/create-bed/", views.ajax_create_bed, name="rooms-ajax-create-bed"),
	path('rooms/api/', include('rooms.api.urls')),
]
