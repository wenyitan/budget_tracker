from flask import Flask, Blueprint
from bot.database import Database 

db = Database()

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.get("/")
def hello_world():
    return db.fetch_all("select * from transactions;")

@transactions_bp.get("/<id>")
def get_transaction_by_id(id):
    transaction = db.fetch_one("select * from transactions where id=?", (id,))
    if transaction:
        return transaction
    else:
        abort(404)