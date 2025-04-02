import sqlite3
from models import Transaction

class Database:
    def __init__(self, db_path="budget_tracker.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def execute(self, query, values=None):
        """Executes an SQL query (INSERT/UPDATE/DELETE)."""
        self.cursor.execute(query, values or ())
        self.conn.commit()

    def fetch_all(self, query, values=None):
        """Fetches all results from a SELECT query."""
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()

