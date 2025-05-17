from flask import Blueprint, request, abort
from flask_httpauth import HTTPBasicAuth
from api.authentication.authentication_helper import AuthenticationHelper
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from config.config import env

def authentication_bp(db):
    authentication_helper = AuthenticationHelper(db)
    authentication_bp = Blueprint('authentication', __name__)
    auth = HTTPBasicAuth()
    
    @authentication_bp.post("/register")
    def register_user():
        if env == "prod":
            abort(403, description="???")
        else:
            usernames = [username['username'] for username in authentication_helper.get_all_usernames()]
            request_body = request.json
            username = request_body["username"]
            if username in usernames:
                return {"error": "Username already exists", "status_code" : 409}, 409
            else:
                password = request_body["password"]
                password_hash = generate_password_hash(password)
                id = authentication_helper.add_user(username, password_hash)
                return {"message": f"Success - user with id {id}, username {username} created", "status_code": 201}, 201

    @auth.verify_password
    def verify_credentials(username, password):
        user = authentication_helper.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None

    @authentication_bp.get("/generate-token")
    @auth.login_required
    def generate_token():
        user = auth.current_user()
        access_token = create_access_token(identity=user['username'])
        return {"message": "Success", "token": access_token, "expiry": 24*60*60, "status_code": 200}, 200

    @auth.error_handler
    def custom_unauthorised():
        return {"error": "Unauthorised access", "status_code": 401}, 401

    @authentication_bp.delete("/delete-user")
    @auth.login_required
    def delete_user():
        user = auth.current_user()
        deleted_user = authentication_helper.delete_user_by_username(user["username"])
        return {"message": f"Success, user with id {deleted_user} has been deleted", "status_code": 200}, 200


    return authentication_bp