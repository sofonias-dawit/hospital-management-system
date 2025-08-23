# backend/api/admin.py

from django.contrib import admin
from .models import (
    Department, 
    Patient, 
    Doctor, 
    Nurse, 
    Receptionist,
    Appointment,
    MedicalRecord,
    Pharmacy,
    Prescription,
    Prescription_Item,
    LabTest,
    Billing,
    Wards_Beds
)

# Register your models here to make them accessible in the Django admin panel.

admin.site.register(Department)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Receptionist)

# Register the missing models
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Pharmacy)
admin.site.register(Prescription)
admin.site.register(Prescription_Item)
admin.site.register(LabTest)
admin.site.register(Billing)
admin.site.register(Wards_Beds)