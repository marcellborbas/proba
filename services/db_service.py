# services/db_service.py
import psycopg2
from config.database import DATABASE_CONFIG

HR_SCHEMA_QUERY = """
SELECT EXISTS(
    SELECT 1 FROM information_schema.schemata 
    WHERE schema_name = 'hr'
);
"""

class DatabaseService:
    """
    🏦 DatabaseService osztály, amely kezeli az adatbázis kapcsolatot és lekérdezéseket.
    🔹 Csatlakozás, séma létrehozás és ellenőrzés, valamint SQL végrehajtás.
    """

    def __init__(self):
        """
        🔧 Inicializálja az adatbázis kapcsolatot és a sémát.
        """
        self.conn = None
        self.connect()
        self.create_schema()  # 📌 Séma létrehozása csatlakozás után
        self._check_schema_exists()  # 📌 Séma létezésének ellenőrzése

    def connect(self):
        """
        🔌 Adatbázis kapcsolat létrehozása a konfiguráció alapján.
        """
        try:
            self.conn = psycopg2.connect(**DATABASE_CONFIG)
            #ez veszélyes, gondolom tranzakció kezelés nem nagyon volt, de jobb lenne kézzel a tranzakciós
            #határokat meghúzni - nice to have
            #tranzakció kezelés megnézése esetleg
            self.conn.autocommit = True
            print("✅ Adatbázis kapcsolat létrejött")
        except Exception as e:
            print(f"❌ Kapcsolódási hiba: {e}")
            raise

    def _check_schema_exists(self):
        """
        🛠️ Ellenőrzi, hogy a 'hr' séma létezik-e az adatbázisban.
        """
        #ezt talán ki lehetne külön emelni valami statikus változóba a fájl elejére
        #nem tudom, hogy pythonban ez mennyire pattern/anti-pattern

        query = HR_SCHEMA_QUERY
        result = self.execute_query(query, fetch_one=True)
        if not result[0]:
            raise RuntimeError("❌ A 'hr' séma nem létezik az adatbázisban!")

    def create_schema(self):
        """
        🏗️ Létrehozza a 'hr' sémát, ha még nem létezik.
        """
        query = "CREATE SCHEMA IF NOT EXISTS hr;"
        self.execute_query(query)
        print("✅ 'hr' séma ellenőrizve/létrehozva")

    def execute_query(self, query, params=None, fetch_one=False):
        """
        🖥️ SQL lekérdezés végrehajtása.
        :param query: Az SQL lekérdezés szövege.
        :param params: Opcionális paraméterek a lekérdezéshez.
        :param fetch_one: Ha igaz, akkor csak egy eredményt ad vissza.
        :return: A lekérdezés eredménye vagy a sorok száma.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params or ())
                if fetch_one:
                    return cur.fetchone()
                return cur.rowcount
        except Exception as e:#fel lehetne több fajta exception-re készíteni - nice to have
            print(f"❌ Lekérdezési hiba: {e}")
            print(f"🧐 Vizsgált lekérdezés: {query}")
            raise

    def close(self):
        """
        🔌 Bezárja az adatbázis kapcsolatot.
        """
        if self.conn and not self.conn.closed:#nice
            self.conn.close()
            print("🔌 Kapcsolat lezárva")
