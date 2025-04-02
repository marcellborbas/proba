# models/department.py

from models.base_model import BaseModel

class Department(BaseModel):
    """
    🏢 Department osztály, amely a HR osztályokat kezeli az adatbázisban.
    🔹 Az osztály az BaseModel-t örökli, így megkapja az alapvető funkciókat.
    """

    # 🏛️ Az adatbázisban található tábla neve
    TABLE_NAME = "hr.departments"

    # 🆔 Az elsődleges kulcs oszlopának neve
    ID_COLUMN = "department_id"

    # 🔍 Az oszlop, amely alapján ellenőrizzük, hogy egy adott osztály már létezik-e
    LOOKUP_COLUMN = "department_name"

    # 📜 SQL lekérdezés a tábla létrehozására, ha még nem létezik
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {ID_COLUMN} SERIAL PRIMARY KEY,  -- Automatikusan növekvő egyedi azonosító
            {LOOKUP_COLUMN} VARCHAR(50) UNIQUE NOT NULL  -- Osztály neve (egyedi és nem lehet NULL)
        );
    """

    # 📥 SQL lekérdezés az új osztályok beszúrására
    INSERT_QUERY = f"""
        INSERT INTO {TABLE_NAME} ({LOOKUP_COLUMN})
        VALUES (%s)
        ON CONFLICT ({LOOKUP_COLUMN}) DO NOTHING  -- Ha már létezik, ne tegyen semmit
        RETURNING {ID_COLUMN};  -- Visszatér a beszúrt rekord ID-jával
    """
