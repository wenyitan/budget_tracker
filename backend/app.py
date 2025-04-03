from flask import Flask
from database import Database
from services import BudgetManager

app = Flask(__name__)
db = Database()
bm = BudgetManager(db)

@app.get('/transactions')
def get_all_transactions():
    return bm.get_all_transactions()


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")