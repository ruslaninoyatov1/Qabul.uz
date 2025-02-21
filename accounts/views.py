from django.shortcuts import render

from rest_framework import generics, permissions, exceptions, status
# from rest_framework.exceptions import NotFound
from rest_framework.response import Response


from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserRetrieveSerializer
# Create your views here.


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {'message': "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.", "user": serializer.data},
            status = status.HTTP_201_CREATED
        )


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


class UserProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = CustomUserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.AuthenticationFailed("Foydalanuvchi autenfikatsiyadan qilinmagan.")
        return user






