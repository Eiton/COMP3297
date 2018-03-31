from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('invite', views.invite, name='invite'),
	path('register', views.register, name='register'),
]