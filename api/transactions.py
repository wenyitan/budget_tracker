from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

def transactions_bp(db):
    transactions_bp = Blueprint('transactions', __name__)

    @transactions_bp.get("/")
    @jwt_required()
    def get_all_transactions():
        current_user = get_jwt_identity()  # Get the current user's identity
        return db.fetch_all("select * from transactions;")

    @transactions_bp.get("/<id>")
    @jwt_required()
    def get_transaction_by_id(id):
        transaction = db.fetch_one("select * from transactions where id=?", (id,))
        if transaction:
            return transaction
        else:
            abort(404)
    
    return transactions_bp