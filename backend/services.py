from models import Transaction
from database import Database

class BudgetManager:
    def __init__(self, db: Database):
        self.db = db

    def log_transaction(self, transaction: Transaction):
        query = "insert into transactions (category, description, amount, person, date) values(:category, :description, :amount, :person, :date)"
        result = self.db.execute(query=query, values=transaction.to_dict())
        last_row_id = result["last_row_id"]
        logged_transaction = self.get_transaction_by_id(last_row_id)
        return {"logged_transaction": logged_transaction}

    def get_transaction_by_id(self, id):
        return self.db.fetch_all("select * from transactions where id=?", (id,))

    def get_all_transactions(self):
        return self.db.fetch_all("select * from transactions")
    
    def delete_transaction_by_id(self, id):
        query = "delete from transactions where id=?"
        result = self.db.execute(query=query, values=(id,))
        affected_rows = result["affected_rows"]
        if affected_rows == 1:
            return f"Transaction with id {id} is deleted!"
        else: 
            return f"Transaction with id {id} not found!"