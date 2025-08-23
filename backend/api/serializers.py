# backend/api/serializers.py

from rest_framework import serializers
from .models import *
from users.models import User

# ... (keep all serializers up to DoctorListSerializer) ...
class UserLiteSerializer(serializers.ModelSerializer):
    class Meta: model = User; fields = ['first_name', 'last_name', 'email']
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta: model = Department; fields = '__all__'
class PatientSerializer(serializers.ModelSerializer):
    class Meta: model = Patient; fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta: model = Doctor; fields = '__all__'
class DoctorListSerializer(serializers.ModelSerializer):
    user_details = UserLiteSerializer(source='user', read_only=True)
    department = serializers.StringRelatedField()
    class Meta: model = Doctor; fields = ['user', 'specialization', 'department', 'user_details']

# --- NEW AND UPDATED SERIALIZERS ---
class NurseSerializer(serializers.ModelSerializer):
    class Meta: model = Nurse; fields = '__all__'

class NurseListSerializer(serializers.ModelSerializer):
    user_details = UserLiteSerializer(source='user', read_only=True)
    class Meta:
        model = Nurse
        fields = ['user', 'shift', 'user_details']

# ... (keep ReceptionistSerializer up to BillingCreateSerializer)
class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta: model = Receptionist; fields = '__all__'
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)
    class Meta: model = Appointment; fields = ['id', 'patient', 'doctor', 'receptionist', 'appointment_date', 'appointment_time', 'status', 'patient_name', 'doctor_name']
class AppointmentCreateSerializer(serializers.ModelSerializer):
    doctor_user_id = serializers.IntegerField(write_only=True)
    class Meta: model = Appointment; fields = ['doctor_user_id', 'appointment_date', 'appointment_time', 'status']
    def create(self, validated_data):
        doctor_user_id = validated_data.pop('doctor_user_id')
        try: doctor_instance = Doctor.objects.get(user_id=doctor_user_id)
        except Doctor.DoesNotExist: raise serializers.ValidationError({"doctor_user_id": "No doctor profile found for this user."})
        appointment = Appointment.objects.create(doctor=doctor_instance, **validated_data)
        return appointment
class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)
    class Meta: model = MedicalRecord; fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment', 'notes', 'record_date', 'patient_name', 'doctor_name']; extra_kwargs = {'patient': {'write_only': True}, 'doctor': {'write_only': True}}
class PharmacySerializer(serializers.ModelSerializer):
    class Meta: model = Pharmacy; fields = '__all__'
class PrescriptionItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    class Meta: model = Prescription_Item; fields = ['medicine', 'medicine_name', 'dosage', 'duration']
class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True)
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), write_only=True, required=False)
    class Meta: model = Prescription; fields = ['id', 'patient', 'doctor', 'prescription_date', 'instructions', 'items', 'patient_name', 'doctor_name']
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        prescription = Prescription.objects.create(**validated_data)
        for item_data in items_data: Prescription_Item.objects.create(prescription=prescription, **item_data)
        return prescription
class MedicalRecordCreateSerializer(serializers.ModelSerializer):
    class Meta: model = MedicalRecord; fields = ['diagnosis', 'treatment', 'notes']
class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    doctor_name = serializers.CharField(source='doctor.__str__', read_only=True)
    class Meta: model = LabTest; fields = ['id', 'patient', 'doctor', 'test_type', 'result', 'status', 'patient_name', 'doctor_name']; extra_kwargs = {'patient': {'write_only': True}, 'doctor': {'write_only': True}}
class BillingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.__str__', read_only=True)
    receptionist_name = serializers.CharField(source='receptionist.__str__', read_only=True, allow_null=True)
    class Meta: model = Billing; fields = ['id', 'patient', 'receptionist', 'amount', 'status', 'bill_date', 'patient_name', 'receptionist_name']
class BillingCreateSerializer(serializers.ModelSerializer):
    class Meta: model = Billing; fields = ['patient', 'amount', 'status']
    
class WardsBedsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    nurse = NurseListSerializer(read_only=True) # Use the detailed nurse serializer
    class Meta: model = Wards_Beds; fields = ['id', 'ward_type', 'status', 'patient', 'nurse']

# New serializer for updating a bed
class WardBedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wards_Beds
        fields = ['patient', 'nurse', 'status']