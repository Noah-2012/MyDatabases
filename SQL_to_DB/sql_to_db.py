import sqlite3
import os

def create_database_from_sql(sql_file_path, db_name='meine_datenbank.db'):
    """
    Erstellt eine SQLite-Datenbank aus einer SQL-Datei.

    Args:
        sql_file_path (str): Der Pfad zur SQL-Datei.
        db_name (str): Der Name der zu erstellenden SQLite-Datenbankdatei.
                       Standardmäßig 'meine_datenbank.db'.
    """
    conn = None  # Initialisierung für den finally-Block
    try:
        # Verbinde zur SQLite-Datenbank.
        # Wenn die Datei nicht existiert, wird sie erstellt.
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Lese den Inhalt der SQL-Datei
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Führe alle SQL-Anweisungen aus.
        # sqlite3.executescript() kann mehrere Anweisungen verarbeiten,
        # die durch Semikolons getrennt sind.
        cursor.executescript(sql_script)

        # Speichere die Änderungen (Commit)
        conn.commit()
        print(f"Datenbank '{db_name}' erfolgreich aus '{sql_file_path}' erstellt.")

    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Datenbank: {e}")
        if conn:
            conn.rollback()  # Rollback bei Fehler
    except FileNotFoundError:
        print(f"Fehler: Die SQL-Datei '{sql_file_path}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        if conn:
            conn.close() # Stelle sicher, dass die Verbindung geschlossen wird

if __name__ == "__main__":
    sql_file = 'tennis.sql'  # Der Name Ihrer SQL-Datei
    database_file = 'tennis_v1.2.db' # Der gewünschte Name für Ihre neue DB

    # Optional: Entferne die alte Datenbankdatei, falls sie existiert
    if os.path.exists(database_file):
        os.remove(database_file)
        print(f"Existierende Datenbankdatei '{database_file}' entfernt.")

    create_database_from_sql(sql_file, database_file)

    # Optional: Überprüfen Sie, ob die Datenbank erstellt wurde und Daten enthält
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        print("\nInhalt der 'nutzer'-Tabelle:")
        cursor.execute("SELECT * FROM matches")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
            
    except sqlite3.Error as e:
        print(f"Fehler beim Überprüfen der Datenbank: {e}")
    finally:
        if conn:
            conn.close()