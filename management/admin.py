from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin, ExportActionMixin

from .models import (PatientCoding, PatientHistory, PatientInformation, PatientLabs, PatientLDA,
                     PatientPostOPComplications, PatientProcedureEvents, PatientVisit, PatientMedication)

# Register your models here.

class PatientCodingResource(resources.ModelResource):
    class Meta:
        model = PatientCoding


class PatientCodingAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PatientCodingResource
    list_display = ("mrn", "source_key", "source_name", "name", "ref_bill_code_set_name", "ref_bill_code")
    search_fields = ("mrn", "source_key", "source_name", "name", "ref_bill_code_set_name", "ref_bill_code")

admin.site.register(PatientCoding, PatientCodingAdmin)


class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ("mrn", "diagnosis_code", "dx_name")

admin.site.register(PatientHistory, PatientHistoryAdmin)

class PatientInformationAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "disch_disp_c", "disch_disp", "hosp_admsn_time", "hosp_disch_time", "los", "icu_admin_flag", "surgery_date")
admin.site.register(PatientInformation, PatientInformationAdmin)

class PatientLabsAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn","enc_type_nm", "lab_code","lab_name", "observation_value","measurement_units", "reference_range","abnormal_flag", "collection_datetime")
admin.site.register(PatientLabs, PatientLabsAdmin)

class PatientLDAAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "description", "properties_display", "site", "placement_instant", "removal_instant", "flo_meas_name", "line_group_name")
admin.site.register(PatientLDA, PatientLDAAdmin)

class PatientPostOPComplicationsAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "element_name", "context_name", "element_abbr", "smrtdta_elem_value")
admin.site.register(PatientPostOPComplications, PatientPostOPComplicationsAdmin)

class PatientProcedureEventsAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "event_display_name", "event_time", "note_text")
admin.site.register(PatientProcedureEvents, PatientProcedureEventsAdmin)

class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "diagnosis_code", "dx_name")
admin.site.register(PatientVisit, PatientVisitAdmin)

class PatientMedicationAdmin(admin.ModelAdmin):
    list_display = ("log_id", "mrn", "ordering_date", "display_name")
admin.site.register(PatientMedication, PatientMedicationAdmin)