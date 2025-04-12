import pytest # type: ignore
from models import Transaction
from services import BudgetManager
from database import Database

db = Database()
bm = BudgetManager(db=db)

new_transaction = Transaction(12.3, "Shopping", "Uniqlo shirts", "Wen Yi", "2025-04-12")

def test_log_transaction_return_dict_with_key_logged_transaction():
    logged_transcation = bm.log_transaction(new_transaction)
    print("Checking if 'logged_transaction' is in dictionary returned")
    assert "logged_transaction" in logged_transcation.keys()
    logged_id = logged_transcation['logged_transaction']['id']
    global logged_transaction_id 
    logged_transaction_id = logged_id

def test_get_transaction_by_id_from_logged_transaction():
    id = logged_transaction_id
    found_transaction = bm.get_transaction_by_id(id)
    assert found_transaction is not None

def test_get_transaction_by_id_check_amount():
    id = logged_transaction_id
    found_transaction = bm.get_transaction_by_id(id)
    assert found_transaction['amount'] == new_transaction.amount

def test_delete_transaction_by_found_id():
    result = bm.delete_transaction_by_id(logged_transaction_id)
    assert result == f"Transaction with id {logged_transaction_id} is deleted!"

def test_delete_transaction_by_unknown_id():
    all_transactions = bm.get_all_transactions()
    id = all_transactions[-1]["id"] + 1 if len(all_transactions) > 0 else logged_transaction_id + 1
    result = bm.delete_transaction_by_id(id)
    assert result == f"Transaction with id {id} not found!"