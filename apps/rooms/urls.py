from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='rooms-index'),
	path('setup/', views.setup, name='rooms-setup'),
]
