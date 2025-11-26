import sqlite3
from datetime import date
import os

# Define the database name
DB_NAME = "./headlines.db"

def get_connection():
    """Establishes a connection to the SQLite database."""
    # Ensure the database file is created in the current working directory
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    
    # This allows accessing columns by name: row['title'] instead of row[1]
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create table with source, title, sentiment, score, and date
    # We use 'date' to track when the scrape happened
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS headlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            sentiment TEXT,
            score REAL,
            date TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {os.path.join(os.getcwd(), DB_NAME)}")

def save_headlines(headlines_data):
    """
    Saves a list of headline dictionaries to the database.
    Expected format: [{'source': '...', 'title': '...', 'sentiment': '...', 'score': 0.5}, ...]
    """
    if not headlines_data:
        print("No headlines to save.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    
    # Get today's date in YYYY-MM-DD format
    today_str = date.today().isoformat()
    
    # Prepare the list of tuples for bulk insertion (executemany is faster)
    data_to_insert = [
        (
            item.get('source', 'Unknown'),
            item.get('title', 'No Title'),
            item.get('sentiment', 'neutral'),
            item.get('score', 0.0),
            today_str
        )
        for item in headlines_data
    ]
    
    try:
        cursor.executemany('''
            INSERT INTO headlines (source, title, sentiment, score, date)
            VALUES (?, ?, ?, ?, ?)
        ''', data_to_insert)
        conn.commit()
        print(f"Successfully saved {len(headlines_data)} headlines to DB.")
    except Exception as e:
        print(f"Error saving headlines: {e}")
    finally:
        conn.close()

def get_headlines_by_date(target_date=None):
    """
    Retrieves headlines for a specific date (YYYY-MM-DD).
    Defaults to today if no date is provided.
    """
    if target_date is None:
        target_date = date.today().isoformat()
        
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM headlines WHERE date = ?", (target_date,))
    rows = cursor.fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to regular dictionaries so Flask can jsonify them easily
    results = [dict(row) for row in rows]
    return results