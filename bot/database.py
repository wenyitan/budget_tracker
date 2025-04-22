import sqlite3
from config import TABLE_NAME

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class Database:
    def __init__(self, db_path="/app/bot/transactions.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

    def execute(self, query, values=None):
        self.cursor.execute(query, values or ())
        self.conn.commit()

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchall()
    
    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values or ())
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()

    def init_db(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTO INCREMENT,
            amount REAL NOT NULL,
            person TEXT NOT NULL,
            date TEXT NOT NULL, 
            category TEXT NOT NULL,
            description TEXT default '',
            shared INTEGER default 1
            );
        """                              # date stored as 'DD-MMM-YYYY' for example '12-Apr-2025', shared is boolean where 1 is true and 0 is false
        self.cursor.execute(create_table_query)