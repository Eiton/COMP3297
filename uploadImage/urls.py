from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='uploadPage'),
	path('upload', views.upload_file, name='upload'),
]