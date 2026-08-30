from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Validate database compatibility before initializing Chroma to prevent locking issues
def _validate_and_cleanup_db(db_path: str):
    import sqlite3
    import json
    import shutil
    import os
    sqlite_file = os.path.join(db_path, "chroma.sqlite3")
    if not os.path.exists(sqlite_file):
        return
    try:
        conn = sqlite3.connect(sqlite_file)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='collections'")
        if cur.fetchone():
            cur.execute("SELECT config_json_str FROM collections")
            for row in cur.fetchall():
                if row[0]:
                    config = json.loads(row[0])
                    if "_type" not in config:
                        conn.close()
                        shutil.rmtree(db_path, ignore_errors=True)
                        return
        conn.close()
    except Exception as e:
        pass

_validate_and_cleanup_db(chroma_path)

vectordb = Chroma(
    persist_directory=chroma_path,
    embedding_function=embedding
)

retriever = vectordb.as_retriever()