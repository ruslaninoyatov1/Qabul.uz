from django.urls import path

from .views import UserRegistrationView

urlpatterns = [
    path('sign-user-up/', UserRegistrationView.as_view(), name='user-sign-up')
]
