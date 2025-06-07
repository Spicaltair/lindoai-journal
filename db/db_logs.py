from .db_core import get_connection

def insert_log(date, start_time, end_time, content, project, recorder):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logs (date, start_time, end_time, content, project, recorder) VALUES (?, ?, ?, ?, ?, ?)",
              (date, start_time, end_time, content, project, recorder))
    c.execute("INSERT INTO phrases (phrase, count) VALUES (?, 1) ON CONFLICT(phrase) DO UPDATE SET count = count + 1",
              (content,))
    conn.commit()
    conn.close()

def get_logs_by_user_date(recorder, date):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT start_time, end_time, content, project
        FROM logs
        WHERE date = ? AND recorder = ?
        ORDER BY start_time
    """, (date, recorder))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_log(recorder, date, start_time, end_time, project, content):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        DELETE FROM logs 
        WHERE recorder = ? AND date = ? AND start_time = ? AND end_time = ? AND project = ? AND content = ?
    """, (recorder, date, start_time, end_time, project, content))
    conn.commit()
    conn.close()
