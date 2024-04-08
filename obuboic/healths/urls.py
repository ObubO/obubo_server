from django.urls import path
from . import views

urlpatterns = [
    path('caregrade/simple/', views.SimpleCareGradeAPI.as_view()),
    path('caregrade/detail/', views.CareGradeAPI.as_view()),

]

