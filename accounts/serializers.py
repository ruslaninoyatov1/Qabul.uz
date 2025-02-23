from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Branch, City

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'username', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date', 'password', 'branch', 'role']
        extra_kwargs ={'password': {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date']


class BranchSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    class Meta:
        model = Branch
        fields = ['id', 'name', 'city', 'city_name']
    

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']




