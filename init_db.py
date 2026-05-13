#!/usr/bin/env python3
"""Initialize database schema"""

from db import engine
from sqlalchemy import text

def init_db():
    with engine.begin() as conn:
        # Read and execute schema
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()

        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

        for statement in statements:
            if statement:
                print(f"Executing: {statement[:50]}...")
                conn.execute(text(statement))

        print("✅ Database schema created successfully!")

if __name__ == "__main__":
    init_db()