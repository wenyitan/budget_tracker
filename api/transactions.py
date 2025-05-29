from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId 
from bson.errors import InvalidId

def transactions_bp(db):
    transactions_bp = Blueprint('transactions', __name__)
    transactions_collection = db.get_collection("transactions")

    @transactions_bp.get("/")
    @jwt_required()
    def get_all_transactions():
        results = transactions_collection.find({})
        return list(results)

    @transactions_bp.get("/<id>")
    @jwt_required()
    def get_transaction_by_id(id):
        transaction = transactions_collection.find_one({"_id": ObjectId(id)})
        if transaction:
            return transaction
        else:
            abort(404)

    @transactions_bp.post("/")
    @jwt_required()
    def add_transaction():
        transaction = request.json
        result = transactions_collection.insert_one(transaction)
        last_row_id = str(result.inserted_id)
        return {"message": "success", "status_code": 201, "transaction": get_transaction_by_id(last_row_id)}, 201

    @transactions_bp.delete("/<id>")
    @jwt_required()
    def delete_transaction_by_id(id):
        try:
            to_delete = ObjectId(id)
        except InvalidId:
            return {"error": "ID not in required format", "status_code": 400}, 400
        result = transactions_collection.delete_one({"_id": ObjectId(id)})
        deleted_count = result.deleted_count
        if deleted_count == 1:
            return {"message": "Success", "status_code": 200, "deleted_count": deleted_count}, 200
        else:
            return {"error": "No documents deleted. Please check the id.", "status_code": 404, "deleted_count": deleted_count}, 404
    return transactions_bp