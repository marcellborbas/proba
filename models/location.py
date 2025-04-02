# models/location.py

from models.base_model import BaseModel

class Location(BaseModel):
    """
    📍 Location osztály, amely a telephelyeket kezeli az adatbázisban.
    🔹 Az osztály a BaseModel-t örökli, így megkapja az alapvető adatbázis műveleteket.
    """

    # 🏛️ Az adatbázisban található tábla neve
    TABLE_NAME = "hr.locations"

    # 🆔 Az elsődleges kulcs oszlopának neve
    ID_COLUMN = "location_id"

    # 🏙️ Az oszlop neve, amely a város nevét tárolja
    LOOKUP_COLUMN = "city"

    # 📜 SQL lekérdezés a tábla létrehozására, ha még nem létezik
    CREATE_TABLE_QUERY = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {ID_COLUMN} SERIAL PRIMARY KEY,  -- Automatikusan növekvő egyedi azonosító
            {LOOKUP_COLUMN} VARCHAR(50) UNIQUE NOT NULL  -- Városnév, egyedi és kötelező
        );
    """

    # 📥 SQL lekérdezés egy új telephely beszúrására
    INSERT_QUERY = f"""
        INSERT INTO {TABLE_NAME} ({LOOKUP_COLUMN})
        VALUES (%s)
        ON CONFLICT ({LOOKUP_COLUMN}) DO NOTHING  -- Ha már létezik, nem szúrja be újra
        RETURNING {ID_COLUMN};  -- Visszatér az újonnan beszúrt rekord ID-jával
    """
