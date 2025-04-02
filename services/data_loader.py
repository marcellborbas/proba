import csv
from models import Department, Job, Location, Salary, Employee

class DataLoader:
    """
    📂 DataLoader osztály felelős az adatok adatbázisba történő betöltéséért.
    🔹 Táblák létrehozása és CSV fájlból történő adatbetöltés.
    """

    def __init__(self, db_service):
        """
        🔧 Inicializálja az adatbázis szolgáltatást.
        :param db_service: Az adatbázis kezelő osztály példánya.
        """
        self.db_service = db_service

    def create_tables(self):
        """
        🛠️ Az adatbázis tábláinak létrehozása az egyes modellek alapján.
        """
        for model in [Department, Job, Location, Salary, Employee]:
            model.create_table(self.db_service)

    def load_data_from_csv(self, file_path):
        """
        📊 CSV fájl beolvasása és az adatok betöltése az adatbázisba.
        :param file_path: A CSV fájl elérési útvonala.
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # 📌 Osztályokba tartozó adatok beszúrása
                department_id = Department.insert_data(self.db_service, (row['department'],))
                job_id = Job.insert_data(self.db_service, (row['job'],))
                location_id = Location.insert_data(self.db_service, (row['location'],))
                salary_id = Salary.insert_data(self.db_service, (int(row['monthly_salary']),))

                # 🚨 Ellenőrzés: ha bármelyik beszúrás sikertelen, a sor kimarad
                if None in (department_id, job_id, location_id, salary_id):
                    print(f"HIBA: Hiányzó érték beszúrásnál: {row}")
                    continue  # Kihagyja ezt a sort és folytatja a következővel

                # 👨‍💼 Dolgozó adatainak beszúrása
                self.insert_employee(row, department_id[0], job_id[0], location_id[0], salary_id[0])

    def insert_employee(self, row, department_id, job_id, location_id, salary_id):
        """
        👨‍💼 Dolgozó adatainak beszúrása az adatbázisba.
        :param row: A dolgozó adatainak egy sora a CSV fájlból.
        :param department_id: A dolgozóhoz tartozó osztály ID-ja.
        :param job_id: A dolgozó munkakörének ID-ja.
        :param location_id: A dolgozó munkavégzési helyének ID-ja.
        :param salary_id: A dolgozó fizetésének ID-ja.
        """
        query = f"""
        INSERT INTO {Employee.TABLE_NAME} (
            first_name, last_name, department_id, job_id, 
            location_id, hire_date, salary_id, absence_days
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (first_name, last_name, hire_date) DO NOTHING;
        """
        params = (
            row['first_name'], row['last_name'], department_id, job_id,
            location_id, row['hire_date'], salary_id, int(row['absence_days'])
        )

        # 🏦 SQL lekérdezés végrehajtása
        self.db_service.execute_query(query, params)
