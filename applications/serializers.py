from rest_framework import serializers
from .models import Application, Document


class DocumentSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Document
        fields = ['id', 'owner', 'owner_username','file', 'uploaded_at']


class ApplicationSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'owner', 'owner_username', 'uploaded_date', 'status']


class ApplicationRetrieveSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'owner', 'owner_username', 'documents', 'uploaded_date', 'status', 'branch', 'branch_name', 'city', 'city_name', 'reason']



