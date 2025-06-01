from database.database import Database
from bot.transaction import Transaction
from config.logging_config import logger
from config.bot_config import DATE_FORMAT, ALLOWED_USERS
from bot.utils import months_day_map
import datetime
from database.aggregates import get_aggregate_for_breakdown_by_month_and_person
from bson import ObjectId

class BudgetManager():
    def __init__(self):
        self.db = Database()
        self.transactions_collection = self.db.get_collection("transactions")
        self.categories_collection = self.db.get_collection("categories")

    def get_all_categories(self):
        results = list(self.categories_collection.find({}))
        return results
    
    def add_new_category(self, category):
        result = self.categories_collection.insert_one({"name": category})
        last_row_id = result.inserted_id
        logger.info(f"database_logger - categories: {self.get_category_by_id(last_row_id)}" )
        return last_row_id
    
    def get_category_by_id(self, id: str):
        result = self.categories_collection.find_one({"_id": ObjectId(id)})
        return result
    
    def get_id_by_category(self, category):
        result = self.categories_collection.find_one({"name": category})
        return result
    
    def delete_category_by_name(self, category) -> None:
        deleted = self.categories_collection.delete_one({"name": category})
    
    def save_transaction(self, transaction: Transaction):
        result = self.transactions_collection.insert_one(transaction.__dict__)
        last_row_id = result.inserted_id
        logger.info(f"database_logger - transaction: {self.get_transaction_by_id(last_row_id)}" )
        return last_row_id
    
    def get_transaction_by_id(self, id: str):
        result = self.transactions_collection.find_one({"_id": ObjectId(id)})
        return result

    def get_transactions_by_month(self, month_str): # %b-%Y eg. May-2025
        results = list(self.transactions_collection.find({"date": {"$regex": f"{month_str}$"}}))
        return results

    def get_current_months_transactions(self):
        now = datetime.datetime.now()
        month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) # %b-%Y
        now_string = now.strftime(month_year_date_format) # e.g. May-2025
        results = self.get_transactions_by_month(now_string)
        return results

    def get_breakdown_by_month_and_person(self, month, person):
        breakdown = self.transactions_collection.aggregate(get_aggregate_for_breakdown_by_month_and_person(month=month, person=person))
        return list(breakdown)[0]
        
    def get_current_months_breakdown_by_id(self, id):
        person = ALLOWED_USERS[str(id)]
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
        results = self.transactions_collection.find({})
        return list(results)
    
    def delete_transaction_by_id(self, id: str) -> None:
        self.transactions_collection.delete_one({"_id": ObjectId(id)})

### "select t.id, t.amount, t.person, t.date, t.description, t.shared, c.category from transactions as t left join categories as c on t.category_id = c.id"