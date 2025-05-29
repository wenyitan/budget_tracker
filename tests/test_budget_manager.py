from bot.budget_manager import BudgetManager
from bot.transaction import Transaction
from bson import ObjectId
from datetime import datetime
from config.bot_config import DATE_FORMAT

bm = BudgetManager()

context = {}

now = datetime.now().strftime(DATE_FORMAT)

def test_add_new_category_and_get_category_and_id():
    print("::group::Adding new category")
    inserted_id = bm.add_new_category("test_placeholder_category")
    print("::notice::Asserting integer returned by add_new_category")
    assert type(inserted_id) == ObjectId
    print("::notice::Retrieving added category using id")
    retrieved_category = bm.get_category_by_id(str(inserted_id))
    print("::notice::Asserting category returned is 'test_placeholder_category'")
    assert retrieved_category['name'] == "test_placeholder_category"
    print("::notice::Retrieving id of added category using category name")
    retrieved_id = bm.get_id_by_category("test_placeholder_category")
    print(f"::notice::Asserting id returned is {inserted_id}")
    assert retrieved_id['_id'] == inserted_id

def test_get_all_category():
    categories = bm.get_all_categories()
    assert "test_placeholder_category" in list(map(lambda cat: cat['name'], categories))

def test_delete_category_by_category_name():
    bm.delete_category_by_name("test_placeholder_category")
    categories = bm.get_all_categories()
    assert "test_placeholder_category" not in list(map(lambda cat: cat['name'], categories))

def test_save_transaction_and_get_transaction_by_id():
    transaction = Transaction(amount=12.4, person="Rando", date=now, description="test_transcation_description", shared=False, category="Tithing")
    inserted_id = bm.save_transaction(transaction)
    retrieved_transaction = bm.get_transaction_by_id(str(inserted_id))
    assert retrieved_transaction['amount'] == 12.4
    assert retrieved_transaction['person'] == "Rando"
    assert retrieved_transaction['date'] == now
    assert retrieved_transaction['description'] == "test_transcation_description"
    assert retrieved_transaction['shared'] == False
    assert retrieved_transaction['category'] == "Tithing"

def test_get_all_transactions_and_delete_transaction_by_id():
    transactions = bm.get_all_transactions()
    assert len(transactions) != 0
    for transaction in transactions:
        if transaction['description'] == "test_transcation_description":
            id = transaction['_id']
            bm.delete_transaction_by_id(transaction['_id'])
            break
    retrieved_transaction = bm.get_transaction_by_id(id)
    assert retrieved_transaction == None

def test_get_current_months_transaction():
    now = datetime.now()
    month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) # %b-%Y
    now_string = now.strftime(month_year_date_format) # e.g. May-2025
    results = bm.get_current_months_transactions()
    all_transactions = bm.get_all_transactions()
    all_months_transactions = [transaction for transaction in all_transactions if transaction['date'].endswith(now_string)]
    assert len(all_months_transactions) == len(results)