from flask import Flask, request
from flask_cors import CORS
from database import Database
from services import BudgetManager
from models import Transaction

app = Flask(__name__)
CORS(app)
db = Database()
bm = BudgetManager(db)

@app.get('/transactions')
def get_all_transactions():
    return bm.get_all_transactions()

@app.post('/transaction')
def log_transaction():
    transaction = Transaction.from_dict(request.get_json())
    return bm.log_transaction(transaction)

@app.delete('/transaction/<int:id>')
def delete_transaction_by_id(id):
    return bm.delete_transaction_by_id(id)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")