# backend/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, PatientViewSet, DoctorViewSet, NurseViewSet,
    ReceptionistViewSet, AppointmentViewSet, MedicalRecordViewSet,
    PharmacyViewSet, PrescriptionViewSet, LabTestViewSet, BillingViewSet,
    WardsBedsViewSet, DoctorPatientsView, PatientMedicalRecordView,
    AnalyticsSummaryView, SymptomCheckerView, UnassignedPatientsView, # Import new view
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet)
router.register(r'nurses', NurseViewSet)
router.register(r'receptionists', ReceptionistViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'pharmacy', PharmacyViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'lab-tests', LabTestViewSet)
router.register(r'billing', BillingViewSet)
router.register(r'wards-beds', WardsBedsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('doctor/patients/', DoctorPatientsView.as_view(), name='doctor-patients-list'),
    path('patients/unassigned/', UnassignedPatientsView.as_view(), name='unassigned-patients-list'), # Add new URL
    path('patients/<int:patient_pk>/records/', PatientMedicalRecordView.as_view(), name='patient-medical-records'),
    path('analytics/summary/', AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('symptom-checker/', SymptomCheckerView.as_view(), name='symptom-checker'),
]