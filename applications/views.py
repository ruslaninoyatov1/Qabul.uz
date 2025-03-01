from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse, Http404

from rest_framework import generics, permissions, filters
from rest_framework.response import Response

from .models import Application, Document
from .serializers import ApplicationSerializer, DocumentSerializer, ApplicationRetrieveSerializer
from accounts.permissions import IsBankOperator, IsGovernmentOfficer, IsBranchAdmin, IsCustomer, IsBranchBoss
from accounts.models import CustomUser, CustomRole

from drf_spectacular.utils import extend_schema

import os
# Create your views here.


@extend_schema(
    summary="Arizalar ro'yxati", 
    description="Barcha arizalarni qaytaradi va post qiladi.",
    methods=['GET', 'POST'])
class ApplicationAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsGovernmentOfficer | IsBranchAdmin | IsCustomer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'city', 'status']
    search_fields = ['branch', 'city', 'status']
    ordering_fields = ['id', 'branch', 'city', 'status']
    ordering = ['id']

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            return Application.objects.filter(branch=user.branch)
        elif user.role == CustomUser.CUSTOMER:
            return Application.objects.filter(user=user)
        return Application.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            serializer.save(branch=user.branch, city=user.branch.city)
        else:
            serializer.save(user=user)


@extend_schema(
    summary="Ariza qaytaradi.", 
    description="Ariza haqida batafsil ma'lumot qaytaradi.",
    methods=['GET', 'PUT', 'DELETE'])
class ApplicationRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationRetrieveSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated | IsGovernmentOfficer | IsBranchAdmin | IsCustomer]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            return Application.objects.filter(branch=user.branch)
        return Application.objects.all()
    
    def perform_update(self, serializer):
        user = self.request.user
        application = self.get_object()
        if user.role == CustomUser.BRANCH_ADMIN and application.branch != user.branch:
            raise PermissionDenied("Siz faqat o'z filialingizdagi arizalarni o'zgartira olasiz.")
        elif user.role == CustomUser.CUSTOMER and application.user != user:
            raise PermissionDenied("Siz faqat o'zingizga tegishli bo'lgan ariza-larni o'zgartira olasiz.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN and instance.branch != user.branch:
            raise PermissionDenied("Siz faqat o'z filialingizdagi arizalarni o'chira olasiz.")
        elif user.role == CustomUser.CUSTOMER and instance.user != user:
            raise PermissionDenied("Siz faqat o'z arizalaringizni o'chira olasiz.")
        instance.delete()


@extend_schema(
    summary="Hujjat-larni qaytaradi.",
    description="Hujjat-larni qaytaradi va yaratadi.",
    methods=['GET', 'POST']
)
class DocumentAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsGovernmentOfficer | IsBranchAdmin | IsCustomer | IsBranchBoss | permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.role.name in [CustomRole.BRANCH_ADMIN, CustomRole.BRANCH_BOSS]:
            return Document.objects.filter(branch=user.branch)
        return Document.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role.name in [CustomRole.BRANCH_ADMIN, CustomRole.BRANCH_BOSS]:
            serializer.save(branch=user.branch, city=user.branch.city)
        if user.role == CustomUser.role.name.CUSTOMER:
            serializer.save(owner=user, branch=user.branch, city=user.branch.city)
        else:
            serializer.save()


@extend_schema(
    summary="Hujjat qaytaradi.",
    description="Hujjat haqida batafsil ma'lumot qaytaradi.",
    methods=['GET', 'PUT', 'DELETE']
)
class DocumentRetrieveAPIView(generics.RetrieveUpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsGovernmentOfficer | IsBranchAdmin | IsBranchBoss | IsCustomer | permissions.IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.role.name in [CustomRole.BRANCH_ADMIN, CustomRole.BRANCH_BOSS]:
            return Document.objects.filter(branch=user.branch)
        if user.role.name == CustomRole.CUSTOMER:
            return Document.objects.filter(user=user)
        return Document.objects.all()
    
    def perform_update(self, serializer):
        user = self.request.user
        document = self.get_object()
        if user.role.name in [CustomRole.BRANCH_ADMIN or CustomRole.BRANCH_BOSS] and not document.applications.filter(branch=user.branch).exists():
            raise PermissionDenied("Siz faqat o'z filialingizdagi arizalarni tahrir qila olasiz.")
        serializer.save()
        
    def retrieve(self, request, *args, **kwargs): # Hujjat-ni yuklab olish xususiyati.
        download = request.query_params.get("download", "").lower() == 'true'
        
        document = self.get_object()

        if download:
            file_path = document.file.path
            print(f"Fayl yo‘li: {file_path}") 
            try:
                return FileResponse(open(file_path, 'rb'), as_attachment=True)
            except FileNotFoundError:
                raise Http404("Fayl topilmadi.")
        return super().retrieve(request, *args, **kwargs)
    
