from django.urls import path, include

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('upload', views.upload, name='upload'),
	path('get', views.get, name='get'),
	path('show', views.show, name='show'),
	# path('login',views.login,name='login'),
	path('register',views.register,name='register'),
	# path('logout',views.logout,name='logout'),
	# path('forget',views.forget,name='forget'),
	# path('send',views.send,name='send'),
]
