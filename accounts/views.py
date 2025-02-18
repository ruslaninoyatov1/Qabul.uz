from django.shortcuts import render

from rest_framework.generics import CreateAPIView

from .models import CustomUser
from .serializers import CustomUserSerializer
# Create your views here.


class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
