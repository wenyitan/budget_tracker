from flask import Flask, abort
from bot.database import Database 

app = Flask(__name__)

db = Database()

@app.get("/transactions")
def hello_world():
    return db.fetch_all("select * from transactions;")

@app.get("/transactions/<id>")
def get_transaction_by_id(id):
    transaction = db.fetch_one("select * from transactions where id=?", (id,))
    if transaction:
        return transaction
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")