
# backend/api/views.py

from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import IsAdmin, IsAdminOrReadOnly, IsDoctor, IsStaffOrReadOnly 
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter # 1. Import SearchFilter

# --- IMPORTS FOR AI ---
import joblib
import os
import numpy as np
from django.conf import settings

# --- UPDATE THIS VIEWSET ---
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [SearchFilter] # 2. Add the filter backend
    search_fields = ['name', 'description'] # 3. Specify which fields to search on

# ... (The rest of the file remains exactly the same) ...
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all(); serializer_class = PatientSerializer; permission_classes = [IsAuthenticated] 
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'list': return DoctorListSerializer
        return DoctorSerializer
class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    def get_serializer_class(self):
        if self.action == 'list': return NurseListSerializer
        return NurseSerializer
class ReceptionistViewSet(viewsets.ModelViewSet):
    queryset = Receptionist.objects.all(); serializer_class = ReceptionistSerializer; permission_classes = [IsAdmin]
class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'create': return AppointmentCreateSerializer
        return AppointmentSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role in ['Admin', 'Receptionist']: return Appointment.objects.all()
        elif user.role == 'Doctor': return Appointment.objects.filter(doctor__user=user)
        elif user.role == 'Patient': return Appointment.objects.filter(patient__user=user)
        return Appointment.objects.none()
    def perform_create(self, serializer):
        if self.request.user.role == 'Patient':
            patient = Patient.objects.get(user=self.request.user)
            serializer.save(patient=patient)
        else: serializer.save()
class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all(); serializer_class = MedicalRecordSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin': return MedicalRecord.objects.all()
        elif user.role == 'Doctor': return MedicalRecord.objects.filter(doctor__user=user)
        elif user.role == 'Patient': return MedicalRecord.objects.filter(patient__user=user)
        return MedicalRecord.objects.none()
class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all(); serializer_class = PharmacySerializer; permission_classes = [IsStaffOrReadOnly]
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin': return Prescription.objects.all()
        elif user.role == 'Doctor': return Prescription.objects.filter(doctor__user=user)
        elif user.role == 'Patient': return Prescription.objects.filter(patient__user=user)
        return Prescription.objects.none()
    def perform_create(self, serializer):
        doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(doctor=doctor)
class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all(); serializer_class = LabTestSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin': return LabTest.objects.all()
        elif user.role == 'Doctor': return LabTest.objects.filter(doctor__user=user)
        elif user.role == 'Patient': return LabTest.objects.filter(patient__user=user)
        return LabTest.objects.none()
class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action == 'create': return BillingCreateSerializer
        return BillingSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['Admin', 'Receptionist']: return Billing.objects.all()
        elif user.role == 'Patient': return Billing.objects.filter(patient__user=user)
        return Billing.objects.none()
    def perform_create(self, serializer):
        receptionist = Receptionist.objects.get(user=self.request.user)
        serializer.save(receptionist=receptionist)
class WardsBedsViewSet(viewsets.ModelViewSet):
    queryset = Wards_Beds.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']: return WardBedUpdateSerializer
        return WardsBedsSerializer
    def get_queryset(self):
        user = self.request.user
        if user.role in ['Admin', 'Doctor', 'Nurse', 'Receptionist']:
            return Wards_Beds.objects.all()
        return Wards_Beds.objects.none()
class UnassignedPatientsView(generics.ListAPIView):
    serializer_class = PatientSerializer; permission_classes = [IsAuthenticated]
    def get_queryset(self):
        assigned_patient_ids = Wards_Beds.objects.filter(patient__isnull=False).values_list('patient_id', flat=True)
        return Patient.objects.exclude(pk__in=assigned_patient_ids)
class DoctorPatientsView(generics.ListAPIView):
    serializer_class = PatientSerializer; permission_classes = [IsAuthenticated, IsDoctor]
    def get_queryset(self):
        doctor = Doctor.objects.get(user=self.request.user); patient_ids = Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True).distinct()
        return Patient.objects.filter(pk__in=patient_ids)
class PatientMedicalRecordView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    def get_serializer_class(self):
        if self.request.method == 'POST': return MedicalRecordCreateSerializer
        return MedicalRecordSerializer
    def get_queryset(self):
        patient_id = self.kwargs['patient_pk']; return MedicalRecord.objects.filter(patient_id=patient_id).order_by('-record_date')
    def perform_create(self, serializer):
        patient_id = self.kwargs['patient_pk']; patient = Patient.objects.get(pk=patient_id); doctor = Doctor.objects.get(user=self.request.user)
        serializer.save(patient=patient, doctor=doctor)
class AnalyticsSummaryView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request, *args, **kwargs):
        patient_count = Patient.objects.count(); doctor_count = Doctor.objects.count(); receptionist_count = Receptionist.objects.count()
        scheduled_appts = Appointment.objects.filter(status='Scheduled').count(); completed_appts = Appointment.objects.filter(status='Completed').count(); cancelled_appts = Appointment.objects.filter(status='Cancelled').count()
        data = { 'user_counts': [{'name': 'Patients', 'count': patient_count}, {'name': 'Doctors', 'count': doctor_count}, {'name': 'Receptionists', 'count': receptionist_count}], 'appointment_status_counts': [{'name': 'Scheduled', 'count': scheduled_appts}, {'name': 'Completed', 'count': completed_appts}, {'name': 'Cancelled', 'count': cancelled_appts}] }
        return Response(data)
class SymptomCheckerView(APIView):
    permission_classes = [IsAuthenticated]
    model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'disease_predictor.joblib'); features_path = os.path.join(settings.BASE_DIR, 'ml_models', 'model_features.joblib')
    model = joblib.load(model_path); model_features = joblib.load(features_path)
    def post(self, request, *args, **kwargs):
        symptoms = request.data.get('symptoms', []); input_vector = [1 if feature in self.model_features else 0 for feature in self.model_features]
        input_data = np.array(input_vector).reshape(1, -1); prediction = self.model.predict(input_data)[0]
        return Response({'predicted_disease': prediction})
    def get(self, request, *args, **kwargs):
        return Response({'available_symptoms': self.model_features})