import sqlite3

def get_connection():
    return sqlite3.connect("log.db")

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # logs 表：包含 recorder
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            content TEXT NOT NULL,
            project TEXT,
            recorder TEXT
        )
    """)

    # meta 表：基础信息
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

    # phrases 表：短语频率统计
    c.execute("""
        CREATE TABLE IF NOT EXISTS phrases (
            phrase TEXT PRIMARY KEY,
            count INTEGER DEFAULT 1
        )
    """)

    # user_projects 表：多用户项目列表
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            project TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
