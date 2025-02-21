from django.urls import path

from .views import UserRegistrationView, UserListView, UserProfileView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('sign-user-up/', UserRegistrationView.as_view(), name='user-sign-up'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users-list/',  UserListView.as_view(), name='users-list'),
    path('my-profile/', UserProfileView.as_view(), name='user-profile')
]
