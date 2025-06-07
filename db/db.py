import sqlite3
from collections import Counter

def get_top_phrases_for_user(username, limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT content FROM logs WHERE username = ?", (username,))
    rows = c.fetchall()
    conn.close()

    # 简单分句统计：按完整内容为单位统计
    contents = [row[0].strip() for row in rows if row[0]]
    counter = Counter(contents)
    most_common = counter.most_common(limit)
    return [phrase for phrase, count in most_common]

def get_connection():
    return sqlite3.connect("log.db")

def get_logs_by_user_date(user, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT start_time, end_time, content, project FROM logs WHERE date = ? AND recorder = ? ORDER BY start_time", (date, user))
    rows = c.fetchall()
    conn.close()
    return rows

def insert_log(date, start_time, end_time, content, project, recorder):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logs (date, start_time, end_time, content, project, recorder) VALUES (?, ?, ?, ?, ?, ?)",
              (date, start_time, end_time, content, project, recorder))
    c.execute("INSERT INTO phrases (phrase, count) VALUES (?, 1) ON CONFLICT(phrase) DO UPDATE SET count = count + 1",
              (content,))
    conn.commit()
    conn.close()
    
    
def delete_log(username, date, start_time, end_time, project, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        DELETE FROM logs 
        WHERE username = ? AND date = ? AND start = ? AND end = ? AND project = ? AND content = ?
    """, (username, date, start_time, end_time, project, content))
    conn.commit()
    conn.close()


def get_projects():
    with open("projects.xml", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
        
