from database.database import Database
from bot.transaction import Transaction
from config.logging_config import logger
try:
    from config.config import DATE_FORMAT
except ModuleNotFoundError:
    import os
    DATE_FORMAT = os.getenv("DATE_FORMAT")
from bot.utils import months_day_map
import datetime
from config.config import ALLOWED_USERS

class BudgetManager():
    def __init__(self):
        self.db = Database()

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
    
    def delete_category_by_name(self, category):
        query = "delete from categories where category=?"
        return self.db.execute(query, (category,))
    
    def save_transaction(self, transaction: Transaction):
        query = "insert into transactions (amount, person, date, description, shared, category_id) values (?,?,?,?,?,?)"
        self.db.execute(query, transaction.get_query_placeholder())
        last_row_id = self.db.cursor.lastrowid
        logger.info(f"database_logger - transaction: {self.get_transaction_by_id(last_row_id)}" )
        return last_row_id
    
    def get_transaction_by_id(self, id):
        query = "select * from transactions where id=?"
        return self.db.fetch_one(query, (id,))

    def get_current_months_transactions(self):
        now = datetime.datetime.now()
        month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) 
        now_string = now.strftime(month_year_date_format)
        query = f"select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id where t.date like '%{now_string}' order by t.date"
        return self.db.fetch_all(query)
    
    # def get_breakdown_by_month_and_year_and_id(self, month, year, id):
    #     if month not in months_day_map.keys():
    #         return None
    #     else:
    #         person = ALLOWED_USERS[id]
    #         date_string = f"%{month}-{str(year)}"
    #         query = "select sum(t.amount) as amount, c.category from transactions as t left join categories as c on t.category_id = c.id where t.date like ? and person = ? group by c.category;"
    #         return self.db.fetch_all(query, (date_string, person))
        
    def get_current_months_breakdown_by_id(self, id):
        person = ALLOWED_USERS[id]
        results = {}
        all_transactions = self.get_current_months_transactions()
        all_transactions = [ transaction for transaction in all_transactions if transaction['person'] == person or transaction['shared'] ]
        shared = 0
        for transaction in all_transactions:
            category = transaction['category']
            amount = transaction['amount']
            amount = amount/2 if transaction['shared'] else amount
            if transaction['shared']:
                shared += amount 
            if category not in results.keys():
                results[category] = amount
            else:
                results[category] += amount
        results['Total'] = sum(results.values())
        results['Shared'] = shared
        return results

    
    def get_all_transactions(self):
        query = 'select * from transactions;'
        return self.db.fetch_all(query)
    
    def delete_transaction_by_id(self, id):
        query = 'delete from transactions where id=?'
        self.db.execute(query, (id,))
        return self.db.cursor.lastrowid

### "select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id"