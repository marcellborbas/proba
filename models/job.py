# models/job.py

from models.base_model import BaseModel

class Job(BaseModel):
    """
    💼 Job osztály, amely a munkaköröket kezeli az adatbázisban.
    🔹 Az osztály a BaseModel-t örökli, így megkapja az alapvető adatbázis műveleteket.
    """

    # 🏛️ Az adatbázisban található tábla neve
    TABLE_NAME = "hr.jobs"

    # 🆔 Az elsődleges kulcs oszlopának neve
    ID_COLUMN = "job_id"

    # 🔍 Az oszlop neve, amely alapján az egyediséget biztosítjuk
    LOOKUP_COLUMN = "job_title"

    # 📜 SQL lekérdezés a tábla létrehozására, ha még nem létezik
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {ID_COLUMN} SERIAL PRIMARY KEY,  -- Automatikusan növekvő egyedi azonosító
            {LOOKUP_COLUMN} VARCHAR(50) UNIQUE NOT NULL  -- Munkakör neve, egyedi és kötelező
        );
    """

    # 📥 SQL lekérdezés egy új munkakör beszúrására
    INSERT_QUERY = f"""
        INSERT INTO {TABLE_NAME} ({LOOKUP_COLUMN})
        VALUES (%s)
        ON CONFLICT ({LOOKUP_COLUMN}) DO NOTHING  -- Ha már létezik, nem szúrja be újra
        RETURNING {ID_COLUMN};  -- Visszatér az újonnan beszúrt rekord ID-jával
    """
