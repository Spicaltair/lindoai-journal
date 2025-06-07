from .db_core import get_connection

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

def delete_project_for_user(username, project):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM user_projects WHERE username = ? AND project = ?", (username, project))
    conn.commit()
    conn.close()

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