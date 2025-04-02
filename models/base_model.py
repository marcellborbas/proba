# models/base_model.py

class BaseModel:
    """
    🔹 Egy absztrakt osztály, amely közös metódusokat biztosít az adatbázisban lévő modellek számára.
    🔹 Az egyes leszármazott osztályoknak meg kell határozniuk a következő attribútumokat:
       - CREATE_TABLE_QUERY: Az adott tábla létrehozására vonatkozó SQL lekérdezés.
       - TABLE_NAME: A tábla neve.
       - INSERT_QUERY: Az adat beszúrására vonatkozó SQL lekérdezés.
       - ID_COLUMN: Az elsődleges kulcs oszlop neve.
       - LOOKUP_COLUMN: Az az oszlop, amely alapján ellenőrizzük, létezik-e már az adott rekord.
    """

    @classmethod
    def create_table(cls, db_service):
        """🛠️ Létrehozza az adott modellt reprezentáló táblát az adatbázisban."""
        try:
            db_service.execute_query(cls.CREATE_TABLE_QUERY)  # SQL lekérdezés végrehajtása
            print(f"{cls.TABLE_NAME} tábla létrehozva")  # Sikeres létrehozás visszajelzése
        except Exception as e:
            print(f"Hiba a {cls.TABLE_NAME} tábla létrehozásakor: {e}")  # Hiba esetén üzenet
            raise  # Az adott hiba tovább dobása

    @classmethod
    def insert_data(cls, db_service, values):
        """📥 Új rekord beszúrása az adott táblába."""
        try:
            # SQL lekérdezés végrehajtása és egy rekord visszakérése
            result = db_service.execute_query(cls.INSERT_QUERY, values, fetch_one=True)
            if not result:
                # Ha az adat már létezik, akkor lekérdezzük az ID-ját
                result = cls._get_existing_id(db_service, values)
            return result  # Visszatér az új vagy meglévő rekord ID-jával
        except Exception as e:
            print(f" Hiba adat beszúrásakor ({cls.TABLE_NAME}): {e}")  # Hibaüzenet
            raise  # Az adott hiba tovább dobása

    @classmethod
    def _get_existing_id(cls, db_service, values):
        """🔍 Lekérdezi a már létező rekord ID-ját az adott táblából."""
        query = f"""
        SELECT {cls.ID_COLUMN} 
        FROM {cls.TABLE_NAME} 
        WHERE {cls.LOOKUP_COLUMN} = %s;
        """
        return db_service.execute_query(query, (values[0],), fetch_one=True)  # Lekérdezés végrehajtása
