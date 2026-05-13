from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
import os

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "Amirtha@134")) 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cropcare")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def save_message(chat_id, role, content, audio_content=None):
    print("🔥 SAVING:", chat_id, role, content)  # DEBUG

    with engine.begin() as conn:  # ✅ THIS IS THE FIX
        conn.execute(
            text("INSERT INTO messages (chat_id, role, content, audio_content) VALUES (:c, :r, :t, :a)"),
            {"c": chat_id, "r": role, "t": content, "a": audio_content}
       
        )


def get_all_chats():
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT chat_id FROM messages
            ORDER BY chat_id DESC
        """))
        return [row[0] for row in result]

def get_chat_messages(chat_id):
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT role, content, audio_content FROM messages WHERE chat_id=:c ORDER BY id"),
            {"c": chat_id}
        )
        return [{"role": r[0], "content": r[1], "audio_content": r[2]} for r in result]

def create_chat(chat_id, title=None):
    """Create a new chat with optional title"""
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO chats (chat_id, title, created_at) VALUES (:c, :t, NOW())"),
            {"c": chat_id, "t": title}
        )

def get_chat_title(chat_id):
    """Get the title of a chat"""
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT title FROM chats WHERE chat_id=:c"),
            {"c": chat_id}
        )
        row = result.fetchone()
        return row[0] if row else None

def get_all_chats_with_titles():
    """Get all chats with their titles"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT c.chat_id, c.title, m.content as first_message
            FROM chats c
            LEFT JOIN messages m ON c.chat_id = m.chat_id
            WHERE m.id = (
                SELECT MIN(id) FROM messages WHERE chat_id = c.chat_id
            )
            ORDER BY c.created_at DESC
        """))
        return [{"chat_id": row[0], "title": row[1], "first_message": row[2]} for row in result]

def update_chat_title(chat_id, title):
    with engine.begin() as conn:
        conn.execute(
            text("""
                UPDATE chats
                SET title = :t
                WHERE chat_id = :c
            """),
            {"t": title, "c": chat_id}
        )
