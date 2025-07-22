from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Branch, City

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'username', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date', 'password', 'branch', 'role']
        extra_kwargs ={'password': {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class CustomUserLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(phone_number=data['phone_number'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Telefon raqam yoki parol noto'g'ri.")
        
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


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




