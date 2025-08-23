# backend/users/serializers.py

from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        role = validated_data.get('role')
        is_staff = role in [User.Role.ADMIN, User.Role.DOCTOR, User.Role.NURSE, User.Role.RECEPTIONIST]
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role,
            is_staff=is_staff
        )
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'first_name', 'last_name', 'is_active')

# --- NEW SERIALIZER FOR UPDATING USERS ---
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Define fields that an admin is allowed to update
        fields = ('email', 'first_name', 'last_name', 'role', 'is_active')
    
    def update(self, instance, validated_data):
        # If role is changed, update staff status accordingly
        role = validated_data.get('role', instance.role)
        instance.is_staff = role in [User.Role.ADMIN, User.Role.DOCTOR, User.Role.NURSE, User.Role.RECEPTIONIST]
        return super().update(instance, validated_data)