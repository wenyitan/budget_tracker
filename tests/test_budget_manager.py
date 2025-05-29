from bot.budget_manager import BudgetManager
from bot.transaction import Transaction
from bson import ObjectId
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config.bot_config import DATE_FORMAT
import pytest

bm = BudgetManager()

context = {}

now = datetime.now().strftime(DATE_FORMAT)

@pytest.fixture
def format_test():
    print("")
    yield
    print("\n=======================================================")

def test_add_new_category_and_get_category_and_id(format_test):
    print("Adding new category: 'test_placeholder_category'")
    inserted_id = bm.add_new_category("test_placeholder_category")
    print("Asserting type of inserted_id == ObjectId")
    assert type(inserted_id) == ObjectId
    retrieved_category = bm.get_category_by_id(str(inserted_id))
    print("Asserting name of retrieved category == 'test_placeholder_category'")
    assert retrieved_category['name'] == "test_placeholder_category"
    retrieved_id = bm.get_id_by_category("test_placeholder_category")
    print(f"Asserting _id of retrieved category == inserted_id: {inserted_id}")
    assert retrieved_id['_id'] == inserted_id


def test_get_all_category(format_test):
    categories = bm.get_all_categories()
    print("Asserting all categories retrieved includes 'test_placeholder_category'")
    assert "test_placeholder_category" in list(map(lambda cat: cat['name'], categories))

def test_delete_category_by_category_name(format_test):
    print("Deleting category: 'test_placeholder_category'")
    bm.delete_category_by_name("test_placeholder_category")
    categories = bm.get_all_categories()
    print("Asserting all categories retrieved no longer includes 'test_placeholder_category'")
    assert "test_placeholder_category" not in list(map(lambda cat: cat['name'], categories))

def test_save_transaction_and_get_transaction_by_id(format_test):
    transaction = Transaction(amount=12.4, person="Rando", date=now, description="test_transaction_description", shared=False, category="Tithing")
    print(f"Inserting new transaction: {transaction.__dict__}")
    inserted_id = bm.save_transaction(transaction)
    retrieved_transaction = bm.get_transaction_by_id(str(inserted_id))
    print("Asserting amount of retrieved transaction == 12.4")
    assert retrieved_transaction['amount'] == 12.4
    print("Asserting person of retrieved transaction == Rando")
    assert retrieved_transaction['person'] == "Rando"
    print(f"Asserting date of retrieved transaction == {now}")
    assert retrieved_transaction['date'] == now
    print("Asserting description of retrieved transaction == 'test_transaction_description'")
    assert retrieved_transaction['description'] == "test_transaction_description"
    print("Asserting shared of retrieved transaction == False")
    assert retrieved_transaction['shared'] == False
    print("Asserting category of retrieved transaction == 'Tithing'")
    assert retrieved_transaction['category'] == "Tithing"

def test_get_current_months_transaction(format_test):
    now = datetime.now()
    month_year_date_format = '-'.join(DATE_FORMAT.split("-")[1:]) # %b-%Y
    now_string = now.strftime(month_year_date_format) # e.g. May-2025
    one_month_ago = datetime.now() - relativedelta(months=1)
    one_month_ago_string = one_month_ago.strftime(DATE_FORMAT)
    print("Adding three transactions from the previous month:")
    for i in range(3):
        transaction = Transaction(amount=12.4 + i, person="Rando", date=one_month_ago_string, description=f"test_transaction_description_{i}", shared=False, category="Tithing")
        print(transaction.__dict__)
        bm.save_transaction(transaction)
    results = bm.get_current_months_transactions()
    all_transactions = bm.get_all_transactions()
    all_months_transactions = [transaction for transaction in all_transactions if transaction['date'].endswith(now_string)]
    expected_length = len(all_months_transactions)
    print(f"Asserting length of list retrieved by get_current_months_transactions() == {expected_length}")
    assert expected_length == len(results)
    print(f"Asserting length of list retrieved by get_current_months_transactions() != number of all transactions: {len(all_transactions)}")
    assert expected_length != len(all_transactions)

def test_get_all_transactions_and_delete_transaction_by_id(format_test):
    transactions = bm.get_all_transactions()
    print("Asserting length of list of retrieved transaction != 0")
    assert len(transactions) != 0
    for transaction in transactions:
        if transaction['description'] == "test_transaction_description":
            id = transaction['_id']
            print(f"Deleting transaction with _id: {id}")
            bm.delete_transaction_by_id(transaction['_id'])
            break
    retrieved_transaction = bm.get_transaction_by_id(id)
    print(f"Asserting retrieved transaction of id {id} is None")
    assert retrieved_transaction == None
