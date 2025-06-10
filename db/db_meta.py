from .db_core import get_connection
def create_meta_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            date TEXT,
            recorder TEXT,
            location TEXT,
            weather TEXT,
            temperature TEXT,
            PRIMARY KEY (date, recorder)
        )
    """)
    conn.commit()
    conn.close()

def save_meta(recorder, date, location, weather, temperature):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        REPLACE INTO meta (date, recorder, location, weather, temperature)
        VALUES (?, ?, ?, ?, ?)
    """, (date, recorder, location, weather, temperature))
    conn.commit()
    conn.close()

def get_meta_for_user(recorder, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT location, recorder, weather, temperature FROM meta WHERE recorder = ? AND date = ?", (recorder, date))
    row = c.fetchone()
    conn.close()
    return row or ("", "", "", "")

