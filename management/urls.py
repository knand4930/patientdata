from django.urls import path

from management.views import FilterAPIDataAPIView, PatientCodingListAPIView, PatientHistoryListAPIView

urlpatterns = [
    path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
    path("get/patient/coding/data/", PatientCodingListAPIView.as_view(), name="PatientCodingListAPIView"),
    path("get/patient/history/data/", PatientHistoryListAPIView.as_view(), name="PatientHistoryListAPIView"),
    # path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
    # path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
    # path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
    # path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
    # path("get/patient/data/", FilterAPIDataAPIView.as_view(), name="FilterAPIDataAPIView"),
]