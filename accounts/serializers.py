from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =['id', 'first_name', 'last_name', 'phone_number', 'city', 'birth_date']
        extra_kwargs ={'password': {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
