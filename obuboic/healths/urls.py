from django.urls import path
from . import views

urlpatterns = [
    path('caregrade/ex/', views.CareGradeExAPI.as_view()),
    path('caregrade/simple/', views.CareGradeSimpleAPI.as_view()),
    path('caregrade/detail/', views.CareGradeDetailAPI.as_view()),

]

