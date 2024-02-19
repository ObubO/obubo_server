from django.contrib import admin
from django.urls import path, include
from rest_framework import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('healths/', include('healths.urls')),

]
