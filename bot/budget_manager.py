from database import Database
from transaction import Transaction
from logging_config import logger
import datetime
from config import DATE_FORMAT
from utils import months_day_map

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

    def get_current_months_transactions(self):
        now = datetime.datetime.now()
        month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) 
        now_string = now.strftime(month_year_date_format)
        query = f"select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id where t.date like '%{now_string}' order by t.date"
        return self.db.fetch_all(query)
    
    def get_breakdown_by_month_and_year(self, month, year):
        if month not in months_day_map.keys():
            return None
        else:
            date_string = f"%{month}-{str(year)}"
            query = "select sum(t.amount) as amount, c.category from transactions as t left join categories as c on t.category_id = c.id where t.date like ? group by c.category;"
            return self.db.fetch_all(query, (date_string,))
        
    def get_current_months_breakdown(self):
        now = datetime.datetime.now()
        month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) 
        now_string = now.strftime(month_year_date_format).split("-")
        return self.get_breakdown_by_month_and_year(now_string[0], now_string[1])

### "select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id"