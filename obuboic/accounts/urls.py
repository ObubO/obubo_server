from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('join/', views.UserCreateView.as_view()),
    path('join/check-login-id/', views.UserCreateView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('token/refresh/', views.CustomTokenRefreshView.as_view()),
    path('profile/', views.AuthView.as_view()),

]

