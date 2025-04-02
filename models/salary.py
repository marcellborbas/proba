# models/salary.py

from models.base_model import BaseModel

class Salary(BaseModel):
    """
    💰 Salary osztály, amely a fizetéseket kezeli az adatbázisban.
    🔹 Az osztály a BaseModel-t örökli, így megkapja az alapvető adatbázis műveleteket.
    """

    # 🏛️ Az adatbázisban található tábla neve
    TABLE_NAME = "hr.salaries"

    # 🆔 Az elsődleges kulcs oszlopának neve
    ID_COLUMN = "salary_id"

    # 💵 Az oszlop neve, amely a fizetés összegét tárolja
    LOOKUP_COLUMN = "monthly_salary"

    # 📜 SQL lekérdezés a tábla létrehozására, ha még nem létezik
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {ID_COLUMN} SERIAL PRIMARY KEY,  -- Automatikusan növekvő egyedi azonosító
            {LOOKUP_COLUMN} INTEGER NOT NULL,  -- Fizetés összege, nem lehet NULL
            UNIQUE({LOOKUP_COLUMN})  -- Egyedi értékek biztosítása a fizetés oszlopban
        );
    """

    # 📥 SQL lekérdezés egy új fizetés beszúrására
    INSERT_QUERY = f"""
        INSERT INTO {TABLE_NAME} ({LOOKUP_COLUMN})
        VALUES (%s)
        ON CONFLICT ({LOOKUP_COLUMN}) DO NOTHING  -- Ha már létezik, nem szúrja be újra
        RETURNING {ID_COLUMN};  -- Visszatér az újonnan beszúrt rekord ID-jával
    """
