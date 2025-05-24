import sqlite3

def get_connection():
    return sqlite3.connect("log.db")

def create_user_projects_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            project TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_projects_for_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT project FROM user_projects WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def add_project_for_user(username, project):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO user_projects (username, project) VALUES (?, ?)", (username, project))
    conn.commit()
    conn.close()