from models import Transaction
from database import Database

class BudgetManager:
    def __init__(self, db: Database):
        self.db = db

    def log_transaction(self, transaction: Transaction):
        query = "insert into transactions (category, description, amount, person, date) values(:category, :description, :amount, :person, :date)"
        self.db.execute(query=query, values=transaction.to_dict())

    def get_all_transactions(self):
        return self.db.fetch_all("select * from transactions")