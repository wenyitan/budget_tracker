import sqlite3
from bot.database_schema import create_table_queries

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

class Database:
    def __init__(self, db_path="bot.db"):
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
        for query in create_table_queries:     
            self.cursor.execute(query)

db = Database()
db.init_db()