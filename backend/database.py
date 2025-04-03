import sqlite3
from models import Transaction

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class Database:
    def __init__(self, db_path="budget_tracker.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def execute(self, query, values=None):
        """Executes an SQL query (INSERT/UPDATE/DELETE)."""
        executed = self.cursor.execute(query, values or ())
        self.conn.commit()
        return {
            "affected_rows": executed.rowcount,
            "last_row_id": executed.lastrowid
            }

    def fetch_all(self, query, values=None):
        """Fetches all results from a SELECT query."""
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()

