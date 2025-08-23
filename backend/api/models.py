# backend/api/models.py

from django.db import models
from users.models import User

# ... (keep all models up to Prescription_Item as they are) ...
class Department(models.Model):
    name = models.CharField(max_length=100); description = models.TextField(blank=True, null=True)
    def __str__(self): return self.name
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True); name = models.CharField(max_length=100); age = models.IntegerField(null=True, blank=True); gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]); contact = models.CharField(max_length=50, null=True, blank=True); insurance_id = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self): return self.name
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True); department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True); specialization = models.CharField(max_length=100); schedule = models.TextField(blank=True, null=True)
    def __str__(self): return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"
class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True); department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True); shift = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self): return f"Nurse {self.user.first_name} {self.user.last_name}"
class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True); name = models.CharField(max_length=100); contact = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self): return self.name
class Appointment(models.Model):
    STATUS_CHOICES = [('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]; patient = models.ForeignKey(Patient, on_delete=models.CASCADE); doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE); receptionist = models.ForeignKey(Receptionist, on_delete=models.SET_NULL, null=True, blank=True); appointment_date = models.DateField(); appointment_time = models.TimeField(); status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    def __str__(self): return f"Appointment for {self.patient.name} with {self.doctor} on {self.appointment_date}"
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE); doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE); diagnosis = models.TextField(); treatment = models.TextField(); notes = models.TextField(blank=True, null=True); record_date = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Record for {self.patient.name} on {self.record_date.strftime('%Y-%m-%d')}"
class Pharmacy(models.Model):
    name = models.CharField(max_length=100); stock = models.PositiveIntegerField(default=0); expiry_date = models.DateField()
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Pharmacy"
class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE); doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE); prescription_date = models.DateTimeField(auto_now_add=True); instructions = models.TextField()
    def __str__(self): return f"Prescription for {self.patient.name} on {self.prescription_date.strftime('%Y-%m-%d')}"
class Prescription_Item(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='items', on_delete=models.CASCADE); medicine = models.ForeignKey(Pharmacy, on_delete=models.CASCADE); dosage = models.CharField(max_length=50); duration = models.CharField(max_length=50)
    def __str__(self): return f"{self.medicine.name} for Prescription ID: {self.prescription.id}"

# --- UPDATED MODEL ---
class LabTest(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('In-Progress', 'In-Progress'), ('Completed', 'Completed')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=100)
    # Change TextField to FileField to handle uploads
    result = models.FileField(upload_to='lab_reports/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def __str__(self): return f"{self.test_type} for {self.patient.name}"

# ... (keep Billing and Wards_Beds models as they are) ...
class Billing(models.Model):
    STATUS_CHOICES = [('Paid', 'Paid'), ('Unpaid', 'Unpaid')]; patient = models.ForeignKey(Patient, on_delete=models.CASCADE); receptionist = models.ForeignKey(Receptionist, on_delete=models.SET_NULL, null=True); amount = models.DecimalField(max_digits=10, decimal_places=2); status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid'); bill_date = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Bill for {self.patient.name} - Amount: {self.amount}"
    class Meta: verbose_name_plural = "Billing"
class Wards_Beds(models.Model):
    WARD_CHOICES = [('ICU', 'ICU'), ('General', 'General'), ('Private', 'Private')]; STATUS_CHOICES = [('Available', 'Available'), ('Occupied', 'Occupied')]; patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True); nurse = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True, blank=True); ward_type = models.CharField(max_length=20, choices=WARD_CHOICES, default='General'); status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    def __str__(self): return f"Bed {self.id} ({self.ward_type}) - {self.status}"
    class Meta: verbose_name_plural = "Wards & Beds"