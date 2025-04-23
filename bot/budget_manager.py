from database import Database
from transaction import Transaction
from logging_config import logger

class BudgetManager():
    def __init__(self, database: Database):
        self.db = database

    def get_all_categories(self):
        query = f"select * from categories;"
        return self.db.fetch_all(query=query)
    
    def add_new_category(self, category):
        query = f"insert into categories (category) values (?)"
        self.db.execute(query, (category,))
        last_row_id = self.db.cursor.lastrowid
        logger.info(f"database_logger - categories: {self.get_category_by_id(last_row_id)}" )
        return last_row_id
    
    def get_category_by_id(self, id):
        query = "select category from categories where id=?"
        return self.db.fetch_one(query, (id,))
    
    def get_id_by_category(self, category):
        query = "select id from categories where category=?"
        return self.db.fetch_one(query, (category,))
    
    def save_transaction(self, transaction: Transaction):
        query = "insert into transactions (amount, person, date, description, shared, category_id) values (?,?,?,?,?,?)"
        self.db.execute(query, transaction.get_query_placeholder())
        last_row_id = self.db.cursor.lastrowid
        logger.info(f"database_logger - transaction: {self.get_transaction_by_id(last_row_id)}" )
        return last_row_id
    
    def get_transaction_by_id(self, id):
        query = "select * from transactions where id=?"
        return self.db.fetch_one(query, (id,))


### "select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id"