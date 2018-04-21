from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='uploadPage'),
	path('upload', views.upload_file, name='upload'),
	path('download/<pk>', views.download, name='download'),
	path('delete/<pk>',views.delete, name='deleteImage'),
	path('like/<pk>',views.like, name='like'),
	path('imageInfo/<pk>',views.imageInfo, name='like'),
]
