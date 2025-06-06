import sqlite3

def get_connection():
    return sqlite3.connect("log.db")

def create_meta_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_meta (
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT,
            weather TEXT,
            temperature TEXT,
            PRIMARY KEY (username, date)
        )
    """)
    conn.commit()
    conn.close()

def save_meta(username, date, location, weather, temperature):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO user_meta (username, date, location, weather, temperature)
        VALUES (?, ?, ?, ?, ?)
    """, (username, date, location, weather, temperature))
    conn.commit()
    conn.close()

def get_meta_for_user(username, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT location, weather, temperature FROM user_meta
        WHERE username = ? AND date = ?
    """, (username, date))
    row = c.fetchone()
    conn.close()
    return row if row else ("", "", "")
