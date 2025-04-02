# main.py

import sys  # A Python rendszerfüggvényeinek eléréséhez
import os  # Fájl- és útvonalkezeléshez szükséges modul
from services.db_service import DatabaseService  # Az adatbázis-kezelő szolgáltatás importálása
from services.data_loader import DataLoader  # Az adatbetöltő szolgáltatás importálása

def main():
    try:
        # 🔹 Az aktuális fájl könyvtárának elérési útját hozzáadjuk a rendszerútvonalhoz.
        # Ez biztosítja, hogy a program helyesen importálja a csomagokat és modulokat.
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))#ez az importokhoz szükséges?

        # 🔹 Adatbázis-szolgáltatás példányosítása
        # Ez a DatabaseService osztály példányát hozza létre, amely kezeli az adatbázis-kapcsolatot.
        db_service = DatabaseService()

        # 🔹 Adatbetöltő példányosítása
        # A DataLoader felelős az adatbázis tábláinak létrehozásáért és az adatok betöltéséért.
        data_loader = DataLoader(db_service)

        print("\n Táblák létrehozása...")
        # 🔹 Az adatbázis tábláinak létrehozása
        data_loader.create_tables()

        print("\n Adatok betöltése...")
        # 🔹 Adatok betöltése a megadott CSV fájlból
        data_loader.load_data_from_csv('data/Denormaliz_lt_HR_adatok.csv')

        print("\n Minden művelet sikeresen befejeződött!")

    except Exception as e:
        # 🔹 Hiba esetén kiírjuk a hibaüzenetet
        print(f"\n Váratlan hiba: {e}")

    finally:
        # 🔹 Az adatbázis-kapcsolat bezárása a program végén, ha a `db_service` létrejött
        if 'db_service' in locals():# ezzel csekkolja, hogy biztosan létezik-e a változó?
            db_service.close()

# 🔹 A főprogram indítása
if __name__ == "__main__":
    main()
