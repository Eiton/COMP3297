from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),  
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),  
	path('profile/<username>', views.profile, name='profile'),  
	path('invite', views.invite, name='invite'),
	path('register', views.register, name='register'),
	path('forgotPassword', views.forgotPassword, name='forgotPassword'),
	path('resetPassword', views.resetPassword, name='resetPassword'),
	path('changePassword', views.changePassword, name='changePassword'),
	path('upload', views.uploadPage, name='uploadPage'),
	path('download/<pk>', views.download, name='download'),
	path('delete/<pk>',views.delete, name='deleteImage'),
	path('like/<pk>',views.like, name='like'),
]