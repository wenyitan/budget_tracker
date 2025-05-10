from database.database import Database
from flask import Flask
from api.authentication.authentication import authentication_bp
from api.transactions import transactions_bp
from flask_jwt_extended import JWTManager
from config.config import JWT_SECRET_KEY
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # All tokens will expire in 1 hour
    jwt = JWTManager(app)
    db = Database()
    app.register_blueprint(transactions_bp(db), url_prefix='/api/v1/transactions/')
    app.register_blueprint(authentication_bp(db), url_prefix='/api/v1/authentication/')

    return app