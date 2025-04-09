import uuid

from django.db import models

# Create your models here.



class PatientCoding(models.Model):
    mrn	 = models.TextField(default=None, blank=True, null=True)
    source_key	 = models.TextField(default=None, blank=True, null=True)
    source_name	 = models.TextField(default=None, blank=True, null=True)
    name	 = models.TextField(default=None, blank=True, null=True)
    ref_bill_code_set_name	 = models.TextField(default=None, blank=True, null=True)
    ref_bill_code	 = models.TextField(default=None, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ["-create_at"]
        db_table = "management_patientcoding"


class PatientHistory(models.Model):
    mrn = models.TextField(default=None, blank=True, null=True)
    diagnosis_code = models.TextField(default=None, blank=True, null=True)
    dx_name = models.TextField(default=None, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


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
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)



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
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


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


class PatientLDA(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
