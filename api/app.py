from flask import Flask, abort
from bot.database import Database 
from api.transactions import transactions_bp

app = Flask(__name__)
app.register_blueprint(transactions_bp, url_prefix='/api/v1/transactions/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")