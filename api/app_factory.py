from database.database import Database
from flask import Flask
from api.authentication import authentication_bp
from api.transactions import transactions_bp

def create_app():
    app = Flask(__name__)
    db = Database()
    app.register_blueprint(transactions_bp(db), url_prefix='/api/v1/transactions/')
    app.register_blueprint(authentication_bp(db), url_prefix='/api/v1/authentication/')

    return app