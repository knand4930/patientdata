
from django.db import models

# Create your models here.



class PatientCoding(models.Model):
    mrn	 = models.TextField(default=None, blank=True, null=True)
    source_key	 = models.TextField(default=None, blank=True, null=True)
    source_name	 = models.TextField(default=None, blank=True, null=True)
    name	 = models.TextField(default=None, blank=True, null=True)
    ref_bill_code_set_name	 = models.TextField(default=None, blank=True, null=True)
    ref_bill_code	 = models.TextField(default=None, blank=True, null=True)

    class Meta:
        # ordering = ["-create_at"]
        db_table = "management_patientcoding"


class PatientHistory(models.Model):
    mrn = models.TextField(default=None, blank=True, null=True)
    diagnosis_code = models.TextField(default=None, blank=True, null=True)
    dx_name = models.TextField(default=None, blank=True, null=True)



class PatientLabs(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    enc_type_nm = models.TextField(default=None, blank=True, null=True)
    lab_code = models.TextField(default=None, blank=True, null=True)
    lab_name = models.TextField(default=None, blank=True, null=True)
    observation_value = models.TextField(default=None, blank=True, null=True)
    measurement_units = models.TextField(default=None, blank=True, null=True)
    reference_range = models.TextField(default=None, blank=True, null=True)
    abnormal_flag = models.TextField(default=None, blank=True, null=True)
    collection_datetime = models.TextField(default=None, blank=True, null=True)


class PatientLDA(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    description = models.TextField(default=None, blank=True, null=True)
    properties_display = models.TextField(default=None, blank=True, null=True)
    site = models.TextField(default=None, blank=True, null=True)
    placement_instant = models.TextField(default=None, blank=True, null=True)
    removal_instant = models.TextField(default=None, blank=True, null=True)
    flo_meas_name = models.TextField(default=None, blank=True, null=True)
    line_group_name = models.TextField(default=None, blank=True, null=True)


class PatientPostOPComplications(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    element_name = models.TextField(default=None, blank=True, null=True)
    context_name = models.TextField(default=None, blank=True, null=True)
    element_abbr = models.TextField(default=None, blank=True, null=True)
    smrtdta_elem_value = models.TextField(default=None, blank=True, null=True)


class PatientProcedureEvents(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    event_display_name = models.TextField(default=None, blank=True, null=True)
    event_time = models.TextField(default=None, blank=True, null=True)
    note_text = models.TextField(default=None, blank=True, null=True)

class PatientVisit(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    diagnosis_code = models.TextField(default=None, blank=True, null=True)
    dx_name = models.TextField(default=None, blank=True, null=True)


class PatientMedication(models.Model):
    enc_type_c = models.TextField(default=None, blank=True, null=True)
    enc_type_nm = models.TextField(default=None, blank=True, null=True)
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    ordering_date = models.TextField(default=None, blank=True, null=True)
    order_class_nm = models.TextField(default=None, blank=True, null=True)
    medication_id = models.TextField(default=None, blank=True, null=True)
    display_name = models.TextField(default=None, blank=True, null=True)
    medication_nm = models.TextField(default=None, blank=True, null=True)
    start_date = models.TextField(default=None, blank=True, null=True)
    end_date = models.TextField(default=None, blank=True, null=True)
    order_status_nm = models.TextField(default=None, blank=True, null=True)
    record_type = models.TextField(default=None, blank=True, null=True)
    mar_action_nm = models.TextField(default=None, blank=True, null=True)
    med_action_time = models.TextField(default=None, blank=True, null=True)
    admin_sig = models.TextField(default=None, blank=True, null=True)
    dose_unit_nm = models.TextField(default=None, blank=True, null=True)
    med_route_nm = models.TextField(default=None, blank=True, null=True)



class PatientInformation(models.Model):
    log_id = models.TextField(default=None, blank=True, null=True)
    mrn = models.TextField(default=None, blank=True, null=True)
    disch_disp_c = models.TextField(default=None, blank=True, null=True)
    disch_disp = models.TextField(default=None, blank=True, null=True)
    hosp_admsn_time = models.TextField(default=None, blank=True, null=True)
    hosp_disch_time = models.TextField(default=None, blank=True, null=True)
    los = models.TextField(default=None, blank=True, null=True)
    icu_admin_flag = models.TextField(default=None, blank=True, null=True)
    surgery_date = models.TextField(default=None, blank=True, null=True)
    birth_date = models.TextField(default=None, blank=True, null=True)
    height = models.TextField(default=None, blank=True, null=True)
    weight = models.TextField(default=None, blank=True, null=True)
    sex = models.TextField(default=None, blank=True, null=True)
    primary_anes_type_nm = models.TextField(default=None, blank=True, null=True)
    asa_rating_c = models.TextField(default=None, blank=True, null=True)
    asa_rating = models.TextField(default=None, blank=True, null=True)
    patient_class_group = models.TextField(default=None, blank=True, null=True)
    patient_class_nm = models.TextField(default=None, blank=True, null=True)
    primary_procedure_nm = models.TextField(default=None, blank=True, null=True)
    in_or_dttm = models.TextField(default=None, blank=True, null=True)
    out_or_dttm = models.TextField(default=None, blank=True, null=True)
    an_start_datetime = models.TextField(default=None, blank=True, null=True)
    an_stop_datetime = models.TextField(default=None, blank=True, null=True)


class MRNMergeData(models.Model):
    id = models.BigAutoField(primary_key=True)
    model_name = models.TextField(null=True, blank=True)
    models_info = models.TextField(null=True, blank=True)
    mrn = models.TextField(null=True, blank=True, db_index=True)
    source_key = models.TextField(null=True, blank=True)
    source_name = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    ref_bill_code_set_name = models.TextField(null=True, blank=True)
    ref_bill_code = models.TextField(null=True, blank=True)
    diagnosis_code = models.TextField(null=True, blank=True)
    dx_name = models.TextField(null=True, blank=True)
    log_id = models.TextField(null=True, blank=True, db_index=True)
    enc_type_nm = models.TextField(null=True, blank=True)
    lab_code = models.TextField(null=True, blank=True)
    lab_name = models.TextField(null=True, blank=True)
    observation_value = models.TextField(null=True, blank=True)
    measurement_units = models.TextField(null=True, blank=True)
    reference_range = models.TextField(null=True, blank=True)
    abnormal_flag = models.TextField(null=True, blank=True)
    collection_datetime = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    properties_display = models.TextField(null=True, blank=True)
    site = models.TextField(null=True, blank=True)
    placement_instant = models.TextField(null=True, blank=True)
    removal_instant = models.TextField(null=True, blank=True)
    flo_meas_name = models.TextField(null=True, blank=True)
    line_group_name = models.TextField(null=True, blank=True)
    element_name = models.TextField(null=True, blank=True)
    context_name = models.TextField(null=True, blank=True)
    element_abbr = models.TextField(null=True, blank=True)
    smrtdta_elem_value = models.TextField(null=True, blank=True)
    event_display_name = models.TextField(null=True, blank=True)
    event_time = models.TextField(null=True, blank=True)
    note_text = models.TextField(null=True, blank=True)
    enc_type_c = models.TextField(null=True, blank=True)
    ordering_date = models.TextField(null=True, blank=True)
    order_class_nm = models.TextField(null=True, blank=True)
    medication_id = models.TextField(null=True, blank=True)
    display_name = models.TextField(null=True, blank=True)
    medication_nm = models.TextField(null=True, blank=True)
    start_date = models.TextField(null=True, blank=True)
    end_date = models.TextField(null=True, blank=True)
    order_status_nm = models.TextField(null=True, blank=True)
    record_type = models.TextField(null=True, blank=True)
    mar_action_nm = models.TextField(null=True, blank=True)
    med_action_time = models.TextField(null=True, blank=True)
    admin_sig = models.TextField(null=True, blank=True)
    dose_unit_nm = models.TextField(null=True, blank=True)
    med_route_nm = models.TextField(null=True, blank=True)
    disch_disp_c = models.TextField(null=True, blank=True)
    disch_disp = models.TextField(null=True, blank=True)
    hosp_admsn_time = models.TextField(null=True, blank=True)
    hosp_disch_time = models.TextField(null=True, blank=True)
    los = models.TextField(null=True, blank=True)
    icu_admin_flag = models.TextField(null=True, blank=True)
    surgery_date = models.TextField(null=True, blank=True)
    birth_date = models.TextField(null=True, blank=True)
    height = models.TextField(null=True, blank=True)
    weight = models.TextField(null=True, blank=True)
    sex = models.TextField(null=True, blank=True)
    primary_anes_type_nm = models.TextField(null=True, blank=True)
    asa_rating_c = models.TextField(null=True, blank=True)
    asa_rating = models.TextField(null=True, blank=True)
    patient_class_group = models.TextField(null=True, blank=True)
    patient_class_nm = models.TextField(null=True, blank=True)
    primary_procedure_nm = models.TextField(null=True, blank=True)
    in_or_dttm = models.TextField(null=True, blank=True)
    out_or_dttm = models.TextField(null=True, blank=True)
    an_start_datetime = models.TextField(null=True, blank=True)
    an_stop_datetime = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "management_mrnmergedata"
        verbose_name = "MRN Merge Data"
        verbose_name_plural = "MRN Merge Data"
        indexes = [
            models.Index(fields=['mrn']),
            models.Index(fields=['log_id']),
        ]

    def __str__(self):
        return f"MRNMergeData(id={self.id}, mrn={self.mrn})"

