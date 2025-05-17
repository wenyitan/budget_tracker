from flask import Blueprint, abort, request
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

    @transactions_bp.post("/")
    @jwt_required()
    def add_transaction():
        transaction = request.json
        amount = transaction["amount"]
        person = transaction["person"]
        date = transaction["date"]
        description = transaction["description"]
        category_id = transaction["category_id"]
        query = "insert into transactions (amount, person, date, description, category_id) values (?,?,?,?,?)"
        db.execute(query, (amount, person, date, description, category_id))
        last_row_id = db.cursor.lastrowid
        return {"message": "success", "status_code": 201, "transaction": get_transaction_by_id(last_row_id)}, 201
    
    return transactions_bp