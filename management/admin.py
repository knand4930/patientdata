from django.contrib import admin
from .models import PatientCoding, PatientHistory, PatientInformation


# Register your models here.


class PatientCodingAdmin(admin.ModelAdmin):
    list_display = ("id","mrn", "name", "create_at", "update_at")
    list_filter = ("create_at", "update_at")
    search_fields = ("mrn", "source_key", "source_name", "name", "ref_bill_code_set_name", "ref_bill_code")
    date_hierarchy = "create_at"
admin.site.register(PatientCoding, PatientCodingAdmin)

class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ("id","mrn", "dx_name", "create_at", "update_at")
    list_filter = ("create_at", "update_at")
    search_fields = ("mrn", "diagnosis_code", "dx_name")
    date_hierarchy = "create_at"
admin.site.register(PatientHistory, PatientHistoryAdmin)


class PatientInformationAdmin(admin.ModelAdmin):
    list_display = ("id","log_id", "mrn", "sex", "create_at", "update_at")
    list_filter = ("sex","create_at", "update_at")
    search_fields = ("log_id", "mrn", "sex")
    date_hierarchy = "create_at"
admin.site.register(PatientInformation, PatientInformationAdmin)