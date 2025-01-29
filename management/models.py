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
        ordering = ["-create_at"]
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