"""
danbi_backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token, 
    verify_jwt_token,
    refresh_jwt_token
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', obtain_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('routines/', include('routines.urls', namespace='routines')),
]
