# 🚀 Global Memory Setup & Run Guide

## Prerequisites
- Python 3.8+
- PostgreSQL running locally
- `.env` file with API keys

---

## Step 1️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 2️⃣: Create `.env` File

Create a `.env` file in the project root:

```env
# 🔑 API Keys
GOOGLE_API_KEY=your_google_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# 🐘 PostgreSQL Database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cropcare

# 📦 Vector Database (Optional)
VECTOR_DB_PATH=./chat_memory
```

### Get API Keys:
1. **Google Gemini**: https://makersuite.google.com/app/apikeys
2. **Groq**: https://console.groq.com/keys

---

## Step 3️⃣: Set Up PostgreSQL

### If you don't have PostgreSQL:
Download from: https://www.postgresql.org/download/

### Create the database:

```sql
-- In PostgreSQL psql terminal:
CREATE DATABASE cropcare;
```

---

## Step 4️⃣: Initialize Database Tables

Run the setup script to create all required tables:

```bash
python setup_db.py
```

**Expected output:**
```
✅ Created 'chats' table
✅ Created 'messages' table
✅ Created 'user_profile' table
✅ Created index on messages(chat_id)
✅ Created index on messages(created_at)
✅ Created index on chats(created_at)

🎉 Database initialization complete!
Database: cropcare
Host: localhost:5432
User: postgres
```

---

## Step 5️⃣: Run the Streamlit App

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open `http://localhost:8501` in your browser!

---

## ✅ Test Global Memory

Follow these steps in the app:

### Test 1: Store Personal Info
1. Create a new chat
2. Say: **"My name is HASINI and I grow tomatoes"**
3. Bot should acknowledge and remember

### Test 2: Verify Profile
1. Check the **👤 Your Profile** section in the left sidebar
2. You should see your personal information stored

### Test 3: Cross-Chat Memory
1. Create a **new chat** (use the "➕ New Chat" button)
2. Ask: **"What's my name?"**
3. Bot should respond: **"Your name is HASINI"**
4. Ask: **"What do I grow?"**
5. Bot should respond: **"You grow tomatoes"**

### Test 4: Contextual Memory Across Sessions
1. Create another new chat
2. Ask: **"Give me disease treatment for my crop"**
3. Bot should:
   - Remember you grow tomatoes
   - Provide tomato-specific treatment advice
   - Reference previous conversations

---

## 📊 How Memory Flows

```
User says something
        ↓
Saved to PostgreSQL (message table)
        ↓
Embedded and stored in Chroma (vector DB)
        ↓
Metadata added: {"chat_id": X, "type": "user_info" or "chat"}
        ↓
[Next conversation]
        ↓
Bot searches: Global memory + Relevant past + Current chat
        ↓
All retrieved info added to prompt
        ↓
Bot responds with full context awareness
```

---

## 🔍 Database Schema

```sql
-- All chats
SELECT * FROM chats;

-- All messages
SELECT * FROM messages;

-- Search by chat
SELECT * FROM messages WHERE chat_id = 'your-chat-id';

-- Get user info
SELECT * FROM messages WHERE content LIKE '%i am%' 
OR content LIKE '%my name%';
```

---

## 🛠️ Troubleshooting

### ❌ "Connection refused"
- PostgreSQL is not running
- **Fix**: Start PostgreSQL service
  - Windows: Open Services app, restart PostgreSQL
  - Mac: `brew services start postgresql`
  - Linux: `sudo systemctl start postgresql`

### ❌ "Database does not exist"
- Have not created the `cropcare` database
- **Fix**: `CREATE DATABASE cropcare;` in psql

### ❌ "Import langchain_community failed"
- Dependencies not installed
- **Fix**: `pip install langchain-community`

### ❌ "API key not found"
- `.env` file not in project root
- **Fix**: Create `.env` and add your API keys

### ❌ "Chroma connection error"
- Vector database directory doesn't have permissions
- **Fix**: `chmod 777 ./chat_memory` (Linux/Mac)

### ❌ Profile not showing in sidebar
- Chroma database is empty (no conversations yet)
- **Fix**: Have at least one conversation first

---

## 📈 Performance Tips

### For large chat histories:
- Index on `chat_id` is already created (fast queries)
- Vector search is optimized (scores filtered)
- Old data can be archived monthly

### Optimize settings:
In `app.py`, reduce memory retrieval:
```python
# Search fewer items for speed
get_relevant_memory(user_input, chat_id, limit=2)  # was 3
```

---

## 🔐 Data Location

- **Database**: PostgreSQL on `localhost:5432`
- **Vector DB**: `./chat_memory/` directory (local files)
- **Config**: `.env` file (keep secret!)

All data stays on your machine - nothing is sent externally except to your API providers (Google, Groq).

---

## 📚 Next Steps

1. ✅ Test the basic setup
2. 📖 Read [GLOBAL_MEMORY_GUIDE.md](GLOBAL_MEMORY_GUIDE.md) for detailed info
3. 🌱 Start chatting and building your profile!

---

## Support & Debugging

Check these files for errors:
- `setup_db.py` - Database initialization logs
- `.env` - Configuration
- Console output - Streamlit errors

For detailed memory functions, see [db.py](db.py) and [rag_memory.py](rag_memory.py)

Happy farming! 🌱
