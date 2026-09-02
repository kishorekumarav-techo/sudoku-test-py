import sqlite3
from datetime import datetime

DATABASE = "notes.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


def create_note(user_id, content):
    created_at = datetime.utcnow().isoformat()
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (user_id, content, created_at) VALUES (?, ?, ?)",
            (user_id, content, created_at)
        )
        conn.commit()
        return cursor.lastrowid, created_at
    finally:
        conn.close()


def get_notes(user_id, limit, offset):
    conn = get_db_connection()
    try:
        return conn.execute(
            """
            SELECT id, content, created_at
            FROM notes
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (user_id, limit, offset)
        ).fetchall()
    finally:
        conn.close()


def get_note(note_id, user_id):
    conn = get_db_connection()
    try:
        return conn.execute(
            """
            SELECT id, content, created_at
            FROM notes
            WHERE id = ? AND user_id = ?
            """,
            (note_id, user_id)
        ).fetchone()
    finally:
        conn.close()


def update_note(note_id, user_id, content):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE notes
            SET content = ?
            WHERE id = ? AND user_id = ?
            """,
            (content, note_id, user_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()


def delete_note(note_id, user_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM notes WHERE id = ? AND user_id = ?",
            (note_id, user_id)
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
