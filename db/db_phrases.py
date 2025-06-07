from .db_core import get_connection
from collections import Counter

def get_top_phrases_for_user(recorder, limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT content FROM logs WHERE recorder = ?", (recorder,))
    rows = c.fetchall()
    conn.close()

    contents = [row[0].strip() for row in rows if row[0]]
    counter = Counter(contents)
    most_common = counter.most_common(limit)
    return [phrase for phrase, count in most_common]
