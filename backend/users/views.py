# backend/users/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer, UserListSerializer, UserUpdateSerializer
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from api.models import Patient, Doctor, Nurse, Receptionist

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        role = serializer.validated_data.get('role')

        # This logic is now corrected and more robust
        if role == User.Role.DOCTOR:
            Doctor.objects.get_or_create(user=user, defaults={'specialization': 'General Medicine'})
        elif role == User.Role.NURSE:
            Nurse.objects.get_or_create(user=user)
        elif role == User.Role.RECEPTIONIST:
            Receptionist.objects.get_or_create(user=user, defaults={'name': user.username})
        elif role == User.Role.PATIENT:
            Patient.objects.get_or_create(user=user, defaults={'name': user.username})