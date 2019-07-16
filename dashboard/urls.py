from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload, name='upload'),
    path('get', views.get, name='get'),
    path('show', views.show, name='show'),
    path('profile', views.profile, name='profile'),
    path('register', views.register, name='register'),
]
