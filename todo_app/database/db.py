"""
database/db.py
----------------
Handles all SQLite database connectivity and schema setup for the To-Do app.
Keeping this logic separate from app.py keeps the codebase organized and
makes it easy to swap out the storage backend later if needed.
"""

import logging
import sqlite3
import os

logger = logging.getLogger(__name__)

# Path to the SQLite database file (lives inside the "database" folder)
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "todo.db")


def get_connection():
    """
    Create and return a new SQLite connection.
    row_factory is set so query results can be accessed like dictionaries
    (e.g. row["title"] instead of row[0]), which makes template rendering cleaner.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        logger.debug("Opened database connection to %s", DB_PATH)
        return conn
    except sqlite3.Error as e:
        logger.exception("Failed to connect to database")
        raise RuntimeError(f"Failed to connect to database: {e}")


def init_db():
    """
    Create the 'tasks' table if it doesn't already exist.
    Called once when the Flask app starts up.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.exception("Failed to initialize database")
        raise RuntimeError(f"Failed to initialize database: {e}")
    else:
        logger.info("Database initialized successfully at %s", DB_PATH)
    finally:
        conn.close()
