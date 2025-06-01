from bot.budget_manager import BudgetManager
from bot.transaction import Transaction
from bson import ObjectId
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config.bot_config import DATE_FORMAT
import pytest
from pathlib import Path
import json
from tests.bot_tests.budget_manager_breakdown_expected_results import *

bm = BudgetManager()

context = {}

now = datetime.now().strftime(DATE_FORMAT)

test_data_path = Path(__file__).parent.joinpath("budget_manager_test_data.json")

@pytest.fixture(scope="session")
def set_up_and_tear_down():
    test_data = json.load(open(test_data_path, "r"))
    y = bm.transactions_collection.insert_many(test_data)
    print(y.inserted_ids)
    yield
    print("Clearing transactions collection for test db")
    x = bm.transactions_collection.delete_many({})
    print(x.deleted_count, "records deleted")

@pytest.fixture
def format_test():
    print("")
    yield
    print("\n=======================================================")

def test_add_new_category_and_get_category_and_id(format_test, set_up_and_tear_down):
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

def test_get_transactions_by_month(format_test):
    month_str = "May-2025"
    results = bm.get_transactions_by_month(month_str)
    all_transactions = bm.get_all_transactions()
    all_months_transactions = [transaction for transaction in all_transactions if transaction['date'].endswith(month_str)]
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

def test_get_breakdown_by_month_and_person(format_test, set_up_and_tear_down):
    persons = ["test_person_1", "test_person_2", "test_person_1", "test_person_2", "test_person_1", "test_person_2"]
    months = ["Mar-2025", "Mar-2025", "Apr-2025", "Apr-2025", "May-2025", "May-2025"]
    expected_results = [person_1_mar_2025, person_2_mar_2025, person_1_apr_2025, person_2_apr_2025, person_1_may_2025, person_2_may_2025]
    for person, month, expected_result in zip(persons, months, expected_results):
        breakdown = bm.get_breakdown_by_month_and_person(person=person, month=month)
        print(f"\nTesting scenario: Person - {person}, Month - {month}")
        for i in breakdown['breakdown']:
            category = i['_id']
            expected_amount = expected_result[category]
            print(f"Asserting {category} amount == {expected_amount}")
            assert i['total'] == expected_amount
        print(f"Asserting month's total == {expected_result['total']}")
        assert breakdown['total'] == expected_result['total']
        print(f"Asserting month's shared total == {expected_result['shared_total']}")
        assert breakdown['shared_total'] == expected_result['shared_total']
        print(f"Asserting month's unshared total == {expected_result['unshared_total']}")
        assert breakdown['unshared_total'] == expected_result['unshared_total']