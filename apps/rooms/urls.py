from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.index, name='rooms-index'),
	path('setup/', views.setup, name='rooms-setup'),
	path('ajax/create-floor/', views.ajax_create_floor, name='ajax-rooms-create-floor'),
	path('api/', include('rooms.api.urls')),
]
