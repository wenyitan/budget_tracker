from bot.budget_manager import BudgetManager
from bot.transaction import Transaction

bm = BudgetManager()

context = {}

def test_add_new_category_and_get_category_and_id():
    inserted_id = bm.add_new_category("test_placeholder_category")
    assert type(inserted_id) == int
    retrieved_category = bm.get_category_by_id(inserted_id)
    assert retrieved_category['category'] == "test_placeholder_category"
    retrieved_id = bm.get_id_by_category("test_placeholder_category")
    assert retrieved_id['id'] == inserted_id

def test_get_all_category():
    categories = bm.get_all_categories()
    assert "test_placeholder_category" in list(map(lambda cat: cat['category'], categories))

def test_delete_category_by_category_name():
    bm.delete_category_by_name("test_placeholder_category")
    categories = bm.get_all_categories()
    assert "test_placeholder_category" not in list(map(lambda cat: cat['category'], categories))

def test_save_transaction_and_get_transaction_by_id():
    transaction = Transaction(12.4, "Rando", "24-Apr-2025", "test_transcation_description", False, category_id=3)
    inserted_id = bm.save_transaction(transaction)
    retrieved_transaction = bm.get_transaction_by_id(inserted_id)
    assert retrieved_transaction['amount'] == 12.4
    assert retrieved_transaction['person'] == "Rando"
    assert retrieved_transaction['date'] == "24-Apr-2025"
    assert retrieved_transaction['description'] == "test_transcation_description"
    assert retrieved_transaction['shared'] == 0
    assert retrieved_transaction['category_id'] == 3

def test_get_all_transactions_and_delete_transaction_by_id():
    transactions = bm.get_all_transactions()
    assert len(transactions) != 0
    deleted_id = None
    for transaction in transactions:
        if transaction['description'] == "test_transcation_description":
            id = transaction['id']
            deleted_id = bm.delete_transaction_by_id(transaction['id'])
            assert deleted_id == id
            break
    retrieved_transaction = bm.get_transaction_by_id(deleted_id)
    assert retrieved_transaction == None