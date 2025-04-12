# database_handler.py - Manages interaction with the SQLite database

import sqlite3
import os

# Define the directory and the full path for the database
DATABASE_DIR = "data"
DATABASE_PATH = os.path.join(DATABASE_DIR, "anime_scores.db")
TABLE_NAME = "anime_scores"

def setup_database():
    """Sets up the database: creates the directory, connects, and creates the table if it doesn't exist."""
    conn = None
    try:
        # Ensure the database directory exists
        os.makedirs(DATABASE_DIR, exist_ok=True)
        print(f"Ensured database directory '{DATABASE_DIR}' exists.")

        # Connect to the database (creates the file if it doesn't exist in the specified path)
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                title TEXT PRIMARY KEY,
                score REAL NOT NULL
            )
        """)
        conn.commit()
        print(f"Database '{DATABASE_PATH}' setup complete. Table '{TABLE_NAME}' is ready.")

    except sqlite3.Error as e:
        print(f"Database error during setup: {e}")
    except OSError as e:
        print(f"Error creating directory '{DATABASE_DIR}': {e}")
    finally:
        if conn:
            conn.close()

def get_score_from_db(title: str) -> float | None:
    """Retrieves the score for a given title from the database.

    Args:
        title: The anime title to search for.

    Returns:
        The score as a float if found, otherwise None.
    """
    conn = None
    score = None
    try:
        # Connect using the full path
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        # Use parameterized query to prevent SQL injection
        cursor.execute(f"SELECT score FROM {TABLE_NAME} WHERE title = ?", (title,))
        result = cursor.fetchone()
        if result:
            score = result[0]
            # print(f"DEBUG DB: Found score {score} for '{title}' in database.") # Removed debug print
            # print(f"Found score {score} for '{title}' in database.") # Optional: uncomment for debugging
        # else:
            # print(f"Title '{title}' not found in database.") # Optional: uncomment for debugging
    except sqlite3.Error as e:
        print(f"Database error retrieving score for '{title}': {e}")
    finally:
        if conn:
            conn.close()
    return score

def save_score_to_db(title: str, score: float):
    """Saves or updates a title and score in the database.

    Uses INSERT OR REPLACE to handle cases where the title might already exist.

    Args:
        title: The anime title.
        score: The corresponding score.
    """
    conn = None
    try:
        # Connect using the full path
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        # Use INSERT OR REPLACE to add new entries or update existing ones based on the PRIMARY KEY (title)
        cursor.execute(f"INSERT OR REPLACE INTO {TABLE_NAME} (title, score) VALUES (?, ?)", (title, score))
        conn.commit()
        # print(f"Saved/Updated '{title}' with score {score} to database.") # Optional: uncomment for debugging
    except sqlite3.Error as e:
        print(f"Database error saving score for '{title}': {e}")
    finally:
        if conn:
            conn.close() 