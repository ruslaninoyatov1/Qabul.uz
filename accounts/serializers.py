from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'username', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date', 'password']
        extra_kwargs ={'password': {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date']

