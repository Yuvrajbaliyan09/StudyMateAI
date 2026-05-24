import sqlite3


def init_db():
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            notes TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            user_id INTEGER
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        name TEXT,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_session(notes, summary, user_id=None):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (notes, summary, user_id)
        VALUES (?, ?, ?)
    """, (notes, summary, user_id))
    conn.commit()
    session_id = cursor.lastrowid
    conn.close()
    return session_id

def get_sessions(user_id=None):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT id, notes, created_at, name FROM sessions WHERE user_id = ? ORDER BY id DESC", (user_id,))
    else:
        cursor.execute("SELECT id, notes, created_at, name FROM sessions ORDER BY id DESC")
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

def get_quiz_stats(user_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT qr.id, qr.score, qr.total, qr.created_at 
        FROM quiz_results qr
        JOIN sessions s ON qr.session_id = s.id
        WHERE s.user_id = ?
        ORDER BY qr.created_at ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_quiz_result(result_id, user_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM quiz_results 
        WHERE id = ? AND session_id IN (
            SELECT id FROM sessions WHERE user_id = ?
        )
    """, (result_id, user_id))
    conn.commit()
    conn.close()

def reset_quiz_stats(user_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM quiz_results 
        WHERE session_id IN (
            SELECT id FROM sessions WHERE user_id = ?
        )
    """, (user_id,))
    conn.commit()
    conn.close()

def get_or_create_user(google_id, name, email):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (google_id, name, email) VALUES (?, ?, ?)", (google_id, name, email))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect("studymate.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

init_db()