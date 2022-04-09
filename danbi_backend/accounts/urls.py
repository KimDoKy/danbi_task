from django.urls import path
from .views import RegistrationView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
