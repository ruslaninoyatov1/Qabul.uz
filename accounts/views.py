from django.shortcuts import render

from rest_framework import generics, permissions, exceptions, status
# from rest_framework.exceptions import NotFound
from rest_framework.response import Response


from .models import CustomUser, Branch, City
from .serializers import CustomUserSerializer, CustomUserRetrieveSerializer, BranchSerializer, CitySerializer

from drf_spectacular.utils import extend_schema
# Create your views here.


@extend_schema(
    summary="Ro'yxatdan o'tish.",
    description="Foydalanuvchi ro'yxatga oladi.",
    methods=['POST']
)
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


@extend_schema(
    summary="Foydalanuvchilarni qaytaradi",
    description="Foydalanuvchilar ro'yxatini qaytaradi va yaratadi.",
    methods=['GET', 'POST']
)
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]


@extend_schema(
    summary="Foydalanuvchi profili",
    description="Foydalanuvchi qaytaradi va yangilaydi",
    methods=['GET', 'PUT']
)
class UserProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = CustomUserRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.AuthenticationFailed("Foydalanuvchi autenfikatsiyadan qilinmagan.")
        return user


@extend_schema(
    summary="Filiallarni qaytaradi.",
    description="Filiallarni qaytaradi va yaratadi.",
    methods=['GET', 'POST']
)
class BranchAPIView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAdminUser]
    

@extend_schema(
    summary="Shaharlarni qaytaradi",
    description="Shaharlarni qaytaradi va yaratadi.",
    methods=['GET', 'POST']
)
class CityAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAdminUser]





