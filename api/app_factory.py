from database.database import Database
from flask import Flask
from api.authentication.authentication import authentication_bp
from api.transactions import transactions_bp
from flask_jwt_extended import JWTManager
from config.api_config import JWT_SECRET_KEY
from datetime import timedelta
from bson import ObjectId
import json
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def create_app():
    app = Flask(__name__)
    app.json_provider_class = CustomJSONProvider
    app.json = app.json_provider_class(app)    
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # All tokens will expire in 1 hour
    jwt = JWTManager(app)
    db = Database()
    app.register_blueprint(transactions_bp(db), url_prefix='/api/v1/transactions/')
    app.register_blueprint(authentication_bp(db), url_prefix='/api/v1/authentication/')

    return app