import sqlite3


def init_db():
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            notes TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add name column if it doesn't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE sessions ADD COLUMN name TEXT")
    except:
        pass
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            score INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_session(notes, summary):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
        
    cursor.execute("""
        INSERT INTO sessions (notes, summary)
        VALUES (?, ?)
    """, (notes, summary))

    conn.commit()
    session_id = cursor.lastrowid 
    conn.close()
    return session_id

def get_sessions():
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
        
    cursor.execute("SELECT id, notes, created_at, name FROM sessions Order by id DESC")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_session_by_id(session_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id=?", (session_id,))
    session = cursor.fetchone()
    conn.close()
    return session

def delete_session(session_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()
    conn.close()

def rename_session(session_id, new_name):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET name = ? WHERE id = ?", (new_name, session_id))
    conn.commit()
    conn.close()
    
def save_quiz_result(session_id, score, total):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_results (session_id, score, total)
        VALUES (?, ?, ?)
    """, (session_id, score, total))
    conn.commit()
    conn.close()

def get_quiz_stats():
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT score, total, created_at 
        FROM quiz_results 
        ORDER BY created_at ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()