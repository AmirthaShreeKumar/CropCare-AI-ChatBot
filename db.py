from urllib.parse import quote_plus

from sqlalchemy import create_engine, text
import os
import bcrypt

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "Amirtha@134")) 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "cropcare")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def init_db():
    """Initialize the database tables if they don't exist"""
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        # Create chats table with user_id linkage
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id VARCHAR(100) PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                title TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        # Ensure chats table has user_id linkage
        conn.execute(text("ALTER TABLE chats ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id)"))

        # Ensure messages table exists
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                chat_id VARCHAR(100) REFERENCES chats(chat_id),
                role VARCHAR(20),
                content TEXT,
                audio_content TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))

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

def create_chat(chat_id, user_id, title=None):
    """Create or update a chat linked to a specific user"""
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO chats (chat_id, user_id, title, created_at) 
                VALUES (:c, :u, :t, NOW())
                ON CONFLICT (chat_id) DO UPDATE SET 
                    user_id = EXCLUDED.user_id,
                    title = COALESCE(chats.title, EXCLUDED.title)
            """),
            {"c": chat_id, "u": user_id, "t": title}
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

def get_all_chats_with_titles(user_id):
    """Get all chats for a specific user"""
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT c.chat_id, c.title, m.content as first_message
            FROM chats c
            LEFT JOIN messages m ON c.chat_id = m.chat_id
            WHERE c.user_id = :u AND m.id = (
                SELECT MIN(id) FROM messages WHERE chat_id = c.chat_id
            )
            ORDER BY c.created_at DESC
        """), {"u": user_id})
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

def create_user(username, password):
    """Hash password and create a new user"""
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO users (username, password_hash) VALUES (:u, :p)"),
                {"u": username, "p": pwd_hash}
            )
            
            # If this is the first user, migrate all orphaned chats to them
            conn.execute(text("""
                UPDATE chats 
                SET user_id = (SELECT id FROM users ORDER BY id ASC LIMIT 1)
                WHERE user_id IS NULL
            """))
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def authenticate_user(username, password):
    """Verify username and password and return user_id"""
    with engine.begin() as conn:
        result = conn.execute(
            text("SELECT id, password_hash FROM users WHERE username = :u"),
            {"u": username}
        )
        row = result.fetchone()
        if row:
            user_id, stored_hash = row[0], row[1].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                # Only migrate chats to THIS user if they are currently orphaned
                # This helps transition anonymous sessions to the logged-in account
                conn.execute(
                    text("UPDATE chats SET user_id = :uid WHERE user_id IS NULL"),
                    {"uid": user_id}
                )
                return user_id
    return None
