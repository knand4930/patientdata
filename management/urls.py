from django.urls import path

from management.views import PatientCodingListAPIView, PatientHistoryListAPIView, \
    PatientInformationListAPIView, PatientLabsListAPIView, PatientLDAListAPIView, PatientPostOPComplicationsListAPIView, \
    PatientProcedureEventsListAPIView, PatientVisitListAPIView, PatientMedicationListAPIView, MRNFilterListAPIView, \
    SQLMRNFilterListAPIView

urlpatterns = [
    path("get/patient/coding/data/", PatientCodingListAPIView.as_view(), name="PatientCodingListAPIView"),
    path("get/patient/history/data/", PatientHistoryListAPIView.as_view(), name="PatientHistoryListAPIView"),
    path("get/patient/information/data/", PatientInformationListAPIView.as_view(), name="PatientInformationListAPIView"),
    path("get/patient/labs/data/", PatientLabsListAPIView.as_view(), name="PatientLabsListAPIView"),
    path("get/patient/lda/data/", PatientLDAListAPIView.as_view(), name="PatientLDAListAPIView"),
    path("get/patient/complication/data/", PatientPostOPComplicationsListAPIView.as_view(), name="PatientPostOPComplicationsListAPIView"),
    path("get/patient/procedure/data/", PatientProcedureEventsListAPIView.as_view(), name="PatientProcedureEventsListAPIView"),
    path("get/patient/visit/data/", PatientVisitListAPIView.as_view(), name="PatientVisitListAPIView"),
    path("get/patient/medication/data/", PatientMedicationListAPIView.as_view(), name="PatientMedicationListAPIView"),
    path("get/mrn/filter/data/", MRNFilterListAPIView.as_view(), name="MRNFilterListAPIView"),
    path("sql/mrn/filter/data/", SQLMRNFilterListAPIView.as_view(), name="SQLMRNFilterListAPIView"),
]