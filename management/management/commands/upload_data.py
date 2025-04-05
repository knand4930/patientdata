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
                "COPY management_patientlabs (log_id, mrn, enc_type_nm, lab_code, lab_name, observation_value, measurement_units, reference_range, abnormal_flag, collection_datetime) FROM STDIN WITH CSV HEADER",
                f
            )

        # Commit & close
        conn.commit()
        cur.close()
        conn.close()
        print("Upload successful!")
