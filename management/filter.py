from .models import (PatientCoding, PatientHistory, PatientInformation, PatientLabs, PatientLDA,
                     PatientPostOPComplications, PatientProcedureEvents, PatientVisit, PatientMedication)
import django_filters


class PatientCodingFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    class Meta:
        model = PatientCoding
        fields = ["mrn"]

class PatientHistoryFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    class Meta:
        model = PatientHistory
        fields = ["mrn"]

class PatientInformationFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientInformation
        fields = ["mrn", "log_id"]

class PatientLabsFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientLabs
        fields = ["mrn", "log_id"]

class PatientLDAFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientLDA
        fields = ["mrn", "log_id"]

class PatientPostOPComplicationsFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientPostOPComplications
        fields = ["mrn", "log_id"]

class PatientProcedureEventsFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientProcedureEvents
        fields = ["mrn", "log_id"]

class PatientVisitFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientVisit
        fields = ["mrn", "log_id"]

class PatientMedicationFilterSet(django_filters.FilterSet):
    mrn = django_filters.CharFilter(field_name="mrn")
    log_id = django_filters.CharFilter(field_name="log_id")
    class Meta:
        model = PatientMedication
        fields = ["mrn", "log_id"]