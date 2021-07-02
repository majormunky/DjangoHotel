from django.urls import path, include
from . import views


urlpatterns = [
	path('dashboard/', views.index, name='dashboard-index'),
	path('dashboard/setup/', views.setup, name='rooms-setup'),
	path('dashboard/ajax/create-floor/', views.ajax_create_floor, name='ajax-rooms-create-floor'),
	path('rooms/api/', include('rooms.api.urls')),
]
