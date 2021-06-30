from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='rooms-index'),
	path('setup/', views.setup, name='rooms-setup'),
	path('ajax/create-floor/', views.ajax_create_floor, name='ajax-rooms-create-floor'),
]
