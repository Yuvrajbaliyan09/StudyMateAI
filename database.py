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
        
    cursor.execute("SELECT id, notes, created_at FROM sessions Order by id DESC")
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

init_db()