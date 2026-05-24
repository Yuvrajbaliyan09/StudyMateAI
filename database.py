import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres.nvxloynejlgsosejgfwk:YuvrajBaliyan@123@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            google_id TEXT UNIQUE,
            email TEXT,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id SERIAL PRIMARY KEY,
            notes TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id SERIAL PRIMARY KEY,
            session_id INTEGER REFERENCES sessions(id),
            score INTEGER,
            total INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_or_create_user(google_id, email, name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, google_id, email, name FROM users WHERE google_id = %s", (google_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT INTO users (google_id, email, name) VALUES (%s, %s, %s) RETURNING id, google_id, email, name",
            (google_id, email, name)
        )
        user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, google_id, email, name FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def save_session(notes, summary, user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sessions (notes, summary, user_id) VALUES (%s, %s, %s) RETURNING id",
        (notes, summary, user_id)
    )
    session_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return session_id

def get_sessions(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, notes, created_at, name 
        FROM sessions 
        WHERE user_id = %s 
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_session_by_id(session_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, notes, summary, created_at, name, user_id FROM sessions WHERE id = %s", (session_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def delete_session(session_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quiz_results WHERE session_id = %s", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
    conn.commit()
    cursor.close()
    conn.close()

def rename_session(session_id, name):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET name = %s WHERE id = %s", (name, session_id))
    conn.commit()
    cursor.close()
    conn.close()

def save_quiz_result(session_id, score, total):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO quiz_results (session_id, score, total) VALUES (%s, %s, %s)",
        (session_id, score, total)
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_quiz_stats(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT qr.id, qr.score, qr.total, qr.created_at
        FROM quiz_results qr
        JOIN sessions s ON qr.session_id = s.id
        WHERE s.user_id = %s
        ORDER BY qr.created_at ASC
    """, (user_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_quiz_result(result_id, user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM quiz_results 
        WHERE id = %s AND session_id IN (
            SELECT id FROM sessions WHERE user_id = %s
        )
    """, (result_id, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def reset_quiz_stats(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM quiz_results 
        WHERE session_id IN (
            SELECT id FROM sessions WHERE user_id = %s
        )
    """, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()