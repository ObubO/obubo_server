from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join/', views.UserCreateAPI.as_view()),

    path('users/', views.UserListAPI.as_view(), name='UserList'),


]

