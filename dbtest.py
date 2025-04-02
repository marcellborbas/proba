# db_connection_test.py
import psycopg2
from config.database import DATABASE_CONFIG

def test_database_connection():
    """Adatbázis kapcsolat tesztelése"""
    try:
        # Kapcsolódási próbálkozás
        conn = psycopg2.connect(**DATABASE_CONFIG)
        conn.autocommit = True
        
        # Egyszerű lekérdezés futtatása
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            db_version = cur.fetchone()
            print(f"Sikeres kapcsolat! PostgreSQL verzió: {db_version[0]}")
            
            # Ellenőrizzük, hogy létezik-e a hr séma
            cur.execute("SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = 'hr');")
            hr_schema_exists = cur.fetchone()[0]
            print(f"A 'hr' séma létezik: {'Igen' if hr_schema_exists else 'Nem'}")
            
        return True
        
    except psycopg2.OperationalError as e:#valami logger solution jöhetne ide, ha arról volt már szó - nice to have
        print(f"Hiba történt a kapcsolat létrehozásakor: {e}")
        print("\nGyakori okok:")
        print("- Hibás adatbázis név, felhasználónév vagy jelszó")
        print("- A PostgreSQL szerver nem fut")
        print("- Hálózati probléma")
        print("- A config/database_config.py nem megfelelő")
        return False
        
    finally:
        if 'conn' in locals():#itt nem lehet előtte megnzni, hogy nyitott-e?
            conn.close()
            print("Kapcsolat lezárva")

if __name__ == "__main__":
    print("Adatbázis kapcsolat tesztelése...")
    if test_database_connection():
        print("\n✅ Minden rendben, az adatbázissal lehet kapcsolódni!")
    else:
        print("\n❌ Hiba történt, nem sikerült kapcsolódni az adatbázishoz!")