from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection
from django.utils import timezone
import time
import sys


class Command(BaseCommand):
    help = 'Refresh the MRN merge data table by consolidating data from all patient tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before inserting new data',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually executing',
        )
        parser.add_argument(
            '--check-counts',
            action='store_true',
            help='Check record counts in source tables before merging',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=10000,
            help='Batch size for processing (default: 10000)',
        )

    def handle(self, *args, **options):
        start_time = time.time()
        clear_existing = options['clear']
        dry_run = options['dry_run']
        check_counts = options['check_counts']

        self.stdout.write(
            self.style.SUCCESS(f'=== MRN Merge Data Refresh Started at {timezone.now()} ===')
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        try:
            # Check source table counts if requested
            if check_counts:
                self._check_source_counts()

            if not dry_run:
                self._execute_refresh(clear_existing)
            else:
                self._show_dry_run_plan(clear_existing)

            # Calculate execution time
            end_time = time.time()
            execution_time = end_time - start_time

            self.stdout.write(
                self.style.SUCCESS(
                    f'=== Operation completed in {execution_time:.2f} seconds ==='
                )
            )

        except Exception as e:
            raise CommandError(f'Error refreshing merged data: {str(e)}')

    def _check_source_counts(self):
        """Check record counts in all source tables"""
        self.stdout.write('\n--- Source Table Counts ---')

        tables = [
            'management_patientcoding',
            'management_patienthistory',
            'management_patientinformation',
            'management_patientlabs',
            'management_patientmedication',
            'management_patientlda',
            'management_patientpostopcomplications',
            'management_patientprocedureevents',
            'management_patientvisit'
        ]

        total_source_records = 0
        with connection.cursor() as cursor:
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_source_records += count
                self.stdout.write(f'{table}: {count:,} records')

            # Check current merge table count
            cursor.execute("SELECT COUNT(*) FROM management_mrnmergedata")
            current_merge_count = cursor.fetchone()[0]

        self.stdout.write(f'\nTotal source records: {total_source_records:,}')
        self.stdout.write(f'Current merge table records: {current_merge_count:,}')
        self.stdout.write('---\n')

    def _show_dry_run_plan(self, clear_existing):
        """Show what would be executed in dry run mode"""
        self.stdout.write('\n--- Dry Run Plan ---')
        if clear_existing:
            self.stdout.write('1. TRUNCATE management_mrnmergedata table')
        self.stdout.write('2. Execute UNION ALL query to merge data from:')

        tables = [
            ('management_patientcoding', 'PatientCoding'),
            ('management_patienthistory', 'PatientHistory'),
            ('management_patientinformation', 'PatientInformation'),
            ('management_patientlabs', 'PatientLabs'),
            ('management_patientmedication', 'PatientMedication'),
            ('management_patientlda', 'PatientLDA'),
            ('management_patientpostopcomplications', 'PatientPostOPComplications'),
            ('management_patientprocedureevents', 'PatientProcedureEvents'),
            ('management_patientvisit', 'PatientVisit')
        ]

        for table, model_name in tables:
            self.stdout.write(f'   - {table} (as {model_name})')

        self.stdout.write('3. Commit transaction')
        self.stdout.write('---\n')

    def _execute_refresh(self, clear_existing):
        """Execute the actual refresh operation"""
        with transaction.atomic():
            with connection.cursor() as cursor:
                # Optional: Clear existing data
                if clear_existing:
                    self.stdout.write('Clearing existing data...', ending='')
                    sys.stdout.flush()
                    cursor.execute("TRUNCATE TABLE management_mrnmergedata RESTART IDENTITY")
                    self.stdout.write(self.style.WARNING(' Done'))

                # Execute the merge query
                self.stdout.write('Executing merge query...', ending='')
                sys.stdout.flush()

                insert_query = """
                    INSERT INTO management_mrnmergedata (
                        model_name, models_info, mrn, source_key, source_name, name, 
                        ref_bill_code_set_name, ref_bill_code, diagnosis_code, dx_name,
                        log_id, disch_disp_c, disch_disp, hosp_admsn_time, hosp_disch_time,
                        los, icu_admin_flag, surgery_date, birth_date, height, weight, sex,
                        primary_anes_type_nm, asa_rating_c, asa_rating, patient_class_group,
                        patient_class_nm, primary_procedure_nm, in_or_dttm, out_or_dttm,
                        an_start_datetime, an_stop_datetime, enc_type_nm, lab_code, lab_name,
                        observation_value, measurement_units, reference_range, abnormal_flag,
                        collection_datetime, enc_type_c, ordering_date, order_class_nm,
                        medication_id, display_name, medication_nm, start_date, end_date,
                        order_status_nm, record_type, mar_action_nm, med_action_time,
                        admin_sig, dose_unit_nm, med_route_nm, description, properties_display,
                        site, placement_instant, removal_instant, flo_meas_name, line_group_name,
                        element_name, context_name, element_abbr, smrtdta_elem_value,
                        event_display_name, event_time, note_text
                    )

                    SELECT 'PatientCoding' as model_name, 
                           CAST(id AS TEXT) as models_info, 
                           mrn, 
                           source_key, source_name, name, ref_bill_code_set_name, ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           NULL as log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientcoding

                    UNION ALL

                    SELECT 'PatientHistory' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           diagnosis_code, dx_name,
                           NULL as log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patienthistory

                    UNION ALL

                    SELECT 'PatientInformation' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, disch_disp_c, disch_disp, hosp_admsn_time, hosp_disch_time,
                           los, icu_admin_flag, surgery_date, birth_date, height, weight, sex,
                           primary_anes_type_nm, asa_rating_c, asa_rating, patient_class_group,
                           patient_class_nm, primary_procedure_nm, in_or_dttm, out_or_dttm,
                           an_start_datetime, an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientinformation

                    UNION ALL

                    SELECT 'PatientLabs' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, enc_type_nm, lab_code, lab_name,
                           observation_value, measurement_units, reference_range, abnormal_flag,
                           collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientlabs

                    UNION ALL

                    SELECT 'PatientMedication' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, enc_type_c, ordering_date, order_class_nm,
                           medication_id, display_name, medication_nm, start_date, end_date,
                           order_status_nm, record_type, mar_action_nm, med_action_time,
                           admin_sig, dose_unit_nm, med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientmedication

                    UNION ALL

                    SELECT 'PatientLDA' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, description, properties_display,
                           site, placement_instant, removal_instant, flo_meas_name, line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientlda

                    UNION ALL

                    SELECT 'PatientPostOPComplications' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           element_name, context_name, element_abbr, smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientpostopcomplications

                    UNION ALL

                    SELECT 'PatientProcedureEvents' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           NULL as diagnosis_code, NULL as dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           event_display_name, event_time, note_text
                    FROM management_patientprocedureevents

                    UNION ALL

                    SELECT 'PatientVisit' as model_name,
                           CAST(id AS TEXT) as models_info,
                           mrn,
                           NULL as source_key, NULL as source_name, NULL as name, NULL as ref_bill_code_set_name, NULL as ref_bill_code,
                           diagnosis_code, dx_name,
                           log_id, NULL as disch_disp_c, NULL as disch_disp, NULL as hosp_admsn_time, NULL as hosp_disch_time,
                           NULL as los, NULL as icu_admin_flag, NULL as surgery_date, NULL as birth_date, NULL as height, NULL as weight, NULL as sex,
                           NULL as primary_anes_type_nm, NULL as asa_rating_c, NULL as asa_rating, NULL as patient_class_group,
                           NULL as patient_class_nm, NULL as primary_procedure_nm, NULL as in_or_dttm, NULL as out_or_dttm,
                           NULL as an_start_datetime, NULL as an_stop_datetime, NULL as enc_type_nm, NULL as lab_code, NULL as lab_name,
                           NULL as observation_value, NULL as measurement_units, NULL as reference_range, NULL as abnormal_flag,
                           NULL as collection_datetime, NULL as enc_type_c, NULL as ordering_date, NULL as order_class_nm,
                           NULL as medication_id, NULL as display_name, NULL as medication_nm, NULL as start_date, NULL as end_date,
                           NULL as order_status_nm, NULL as record_type, NULL as mar_action_nm, NULL as med_action_time,
                           NULL as admin_sig, NULL as dose_unit_nm, NULL as med_route_nm, NULL as description, NULL as properties_display,
                           NULL as site, NULL as placement_instant, NULL as removal_instant, NULL as flo_meas_name, NULL as line_group_name,
                           NULL as element_name, NULL as context_name, NULL as element_abbr, NULL as smrtdta_elem_value,
                           NULL as event_display_name, NULL as event_time, NULL as note_text
                    FROM management_patientvisit
                """

                # Execute the query
                cursor.execute(insert_query)
                self.stdout.write(self.style.SUCCESS(' Done'))

                # Get the count of inserted records
                cursor.execute("SELECT COUNT(*) FROM management_mrnmergedata")
                total_records = cursor.fetchone()[0]

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully inserted {total_records:,} records into merge table'
                    )
                )