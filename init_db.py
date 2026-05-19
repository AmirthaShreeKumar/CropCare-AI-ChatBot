#!/usr/bin/env python3
"""Initialize database schema"""

from db import engine
from sqlalchemy import text
from src.logger import logger

def init_db():
    with engine.begin() as conn:
        # Read and execute schema
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()

        # Split into individual statements and execute
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]

        for statement in statements:
            if statement:
                logger.info("Executing schema statement: %s", statement[:50])
                conn.execute(text(statement))

        logger.info("✅ Database schema created successfully!")

if __name__ == "__main__":
    init_db()