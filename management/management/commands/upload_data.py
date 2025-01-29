from django.core.management import BaseCommand

csv_path = "/home/ubuntu/Music/ics/EPIC_EMR/EMR/patient_labs.csv"

class Command(BaseCommand):
    help = "insert csv file in data base"
    def handle(self, *args, **options):
        import psycopg2

        # Database connection
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mmOdiM0EAEMljVF7VgWk",
            host="database-1.cxuuke6s0aqw.ap-south-1.rds.amazonaws.com",
            port="5432"
        )
        cur = conn.cursor()

        with open(csv_path, 'r') as f:
            cur.copy_expert(
                "COPY management_patientinformation (log_id, mrn, disch_disp_c, disch_disp, hosp_admsn_time, hosp_disch_time, los, icu_admin_flag, surgery_date, birth_date, height, weight, sex, primary_anes_type_nm, asa_rating_c, asa_rating, patient_class_group, patient_class_nm, primary_procedure_nm, in_or_dttm, out_or_dttm, an_start_datetime, an_stop_datetime) FROM STDIN WITH CSV HEADER",
                f
            )

        # Commit & close
        conn.commit()
        cur.close()
        conn.close()
        print("Upload successful!")
