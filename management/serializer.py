from .models import (PatientCoding, PatientHistory, PatientInformation, PatientLabs, PatientLDA,
                     PatientPostOPComplications, PatientProcedureEvents, PatientVisit, PatientMedication, MRNMergeData)
from rest_framework import serializers

class PatientCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCoding
        fields = "__all__"


class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = "__all__"


class PatientInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInformation
        fields = "__all__"


class PatientLabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientLabs
        fields = "__all__"


class PatientLDASerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientLDA
        fields = "__all__"


class PatientPostOPComplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientPostOPComplications
        fields = "__all__"


class PatientProcedureEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProcedureEvents
        fields = "__all__"


class PatientVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientVisit
        fields = "__all__"


class PatientMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedication
        fields = "__all__"

#
# class MRNMergeDataSerializer(serializers.Serializer):
#     id= serializers.CharField()
#     mrn = serializers.CharField()
#     source_key = serializers.CharField()
#     source_name = serializers.CharField()
#     name = serializers.CharField()
#     ref_bill_code_set_name = serializers.CharField()
#     ref_bill_code = serializers.CharField()
#     diagnosis_code = serializers.CharField()
#     dx_name = serializers.CharField()
#     log_id = serializers.CharField()
#     disch_disp_c = serializers.CharField()
#     hosp_admsn_time = serializers.CharField()
#     hosp_disch_time = serializers.CharField()
#     los = serializers.CharField()
#     icu_admin_flag = serializers.CharField()
#     surgery_date = serializers.CharField()
#     birth_date = serializers.CharField()
#     height = serializers.CharField()
#     weight = serializers.CharField()
#     sex = serializers.CharField()
#     primary_anes_type_nm = serializers.CharField()
#     asa_rating_c = serializers.CharField()
#     asa_rating = serializers.CharField()
#     patient_class_group = serializers.CharField()
#     patient_class_nm = serializers.CharField()
#     primary_procedure_nm = serializers.CharField()
#     in_or_dttm = serializers.CharField()
#     out_or_dttm = serializers.CharField()
#     an_start_datetime = serializers.CharField()
#     an_stop_datetime = serializers.CharField()
#     enc_type_nm = serializers.CharField()
#     lab_code = serializers.CharField()
#     lab_name = serializers.CharField()
#     observation_value = serializers.CharField()
#     measurement_units = serializers.CharField()
#     reference_range = serializers.CharField()
#     abnormal_flag = serializers.CharField()
#     collection_datetime = serializers.CharField()
#     enc_type_c = serializers.CharField()
#     ordering_date = serializers.CharField()
#     order_class_nm = serializers.CharField()
#     medication_id = serializers.CharField()
#     display_name = serializers.CharField()
#     medication_nm = serializers.CharField()
#     start_date = serializers.CharField()
#     end_date = serializers.CharField()
#     order_status_nm = serializers.CharField()
#     record_type = serializers.CharField()
#     mar_action_nm = serializers.CharField()
#     med_action_time = serializers.CharField()
#     admin_sig = serializers.CharField()
#     dose_unit_nm = serializers.CharField()
#     med_route_nm = serializers.CharField()
#     description = serializers.CharField()
#     properties_display = serializers.CharField()
#     site = serializers.CharField()
#     placement_instant = serializers.CharField()
#     removal_instant = serializers.CharField()
#     flo_meas_name = serializers.CharField()
#     line_group_name = serializers.CharField()
#     element_name = serializers.CharField()
#     context_name = serializers.CharField()
#     element_abbr = serializers.CharField()
#     smrtdta_elem_value = serializers.CharField()
#     event_display_name = serializers.CharField()
#     event_time = serializers.CharField()
#     note_text = serializers.CharField()
#
#     class Meta:
#         fields = '__all__'
#
#
#
class MRNMergeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MRNMergeData
        fields = "__all__"

# class MRNMergeDataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MRNMergeData
#         fields = ['id', 'mrn', 'log_id', 'some_other_important_field']