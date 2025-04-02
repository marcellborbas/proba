# models/employee.py

from models.base_model import BaseModel

class Employee(BaseModel):
    """
    👨‍💼 Employee osztály, amely az alkalmazottakat kezeli az adatbázisban.
    🔹 Az osztály a BaseModel-t örökli, így megkapja az alapvető adatbázis műveleteket.
    """

    # 🏛️ Az adatbázisban található tábla neve
    TABLE_NAME = "hr.employees"

    # 🆔 Az elsődleges kulcs oszlopának neve
    ID_COLUMN = "employee_id"

    # 📜 SQL lekérdezés a tábla létrehozására, ha még nem létezik
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {ID_COLUMN} SERIAL PRIMARY KEY,  -- Automatikusan növekvő egyedi azonosító
            
            first_name VARCHAR(50) NOT NULL,  -- Az alkalmazott keresztneve (nem lehet NULL)
            last_name VARCHAR(50) NOT NULL,   -- Az alkalmazott vezetékneve (nem lehet NULL)
            
            department_id INTEGER REFERENCES hr.departments(department_id),  -- Osztály hivatkozás
            job_id INTEGER REFERENCES hr.jobs(job_id),  -- Munkakör hivatkozás
            location_id INTEGER REFERENCES hr.locations(location_id),  -- Munkavégzési hely hivatkozás
            
            hire_date DATE NOT NULL,  -- Felvételi dátum (nem lehet NULL)
            
            salary_id INTEGER REFERENCES hr.salaries(salary_id),  -- Fizetési adatok hivatkozás
            absence_days INTEGER NOT NULL,  -- Hiányzások száma (nem lehet NULL)
            
            UNIQUE(first_name, last_name, hire_date)  -- Egyediség biztosítása adott név és felvételi dátum alapján
        );
    """
