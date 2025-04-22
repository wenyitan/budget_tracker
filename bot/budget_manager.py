from database import Database
from transaction import Transaction

class BudgetManager():
    def __init__(self, database: Database):
        self.db = database

    def get_all_categories(self):
        query = f"select * from categories;"
        return self.db.fetch_all(query=query)
    
    def add_new_category(self, category):
        query = f"insert into categories (category) values (?)"
        self.db.execute(query, (category,))
        return self.db.cursor.lastrowid
    
    def get_category_by_id(self, id):
        query = "select category from categories where id=?"
        return self.db.fetch_one(query, (id,))
    
    def get_id_by_category(self, category):
        query = "select id from categories where category=?"
        return self.db.fetch_one(query, (category,))
    
    def save_transaction(self, transaction: Transaction):
        query = "insert into transactions (amount, person, date, description, shared, category_id) values (?,?,?,?,?,?)"
        self.db.execute(query, transaction.get_query_placeholder())


### "select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id"