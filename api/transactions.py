from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

def transactions_bp(db):
    transactions_bp = Blueprint('transactions', __name__)

    @transactions_bp.get("/")
    @jwt_required()
    def get_all_transactions():
        results = db.get_collection("transactions").find({})
        return list(results)

    @transactions_bp.get("/<id>")
    @jwt_required()
    def get_transaction_by_id(id):
        transaction = db.get_collection("transactions").find_one({"_id": ObjectId(id)})
        if transaction:
            return transaction
        else:
            abort(404)

    @transactions_bp.post("/")
    @jwt_required()
    def add_transaction():
        transaction = request.json
        result = db.get_collection("transactions").insert_one(transaction)
        last_row_id = str(result.inserted_id)
        return {"message": "success", "status_code": 201, "transaction": get_transaction_by_id(last_row_id)}, 201
    
    return transactions_bp