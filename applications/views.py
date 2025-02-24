from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from rest_framework import generics, permissions

from .models import Application, Document
from .serializers import ApplicationSerializer, DocumentSerializer, ApplicationRetrieveSerializer
from accounts.permissions import IsBankOperator, IsGovernmentOfficer, IsBranchAdmin
from accounts.models import CustomUser
# Create your views here.


class ApplicationAPIView(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsGovernmentOfficer | IsBranchAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            return Application.objects.filter(branch=user.branch)
        return Application.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            serializer.save(branch=user.branch, city=user.branch.city)
        else:
            serializer.save()


class ApplicationRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationRetrieveSerializer
    permission_classes = [permissions.IsAdminUser | IsGovernmentOfficer | IsBranchAdmin]

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
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN and instance.branch != user.branch:
            raise PermissionDenied("Siz faqat o'z filialingizdagi arizalarni o'chira olasiz.")
        instance.delete()


class DocumentAPIView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsGovernmentOfficer | IsBranchAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            return Application.objects.filter(branch=user.branch)
        return Application.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == CustomUser.BRANCH_ADMIN:
            serializer.save(branch=user.branch, city=user.branch.city)
        else:
            serializer.save()


