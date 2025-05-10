from flask import Blueprint

def authentication_bp(db):
    authentication_bp = Blueprint('authentication', __name__)
    
    @authentication_bp.post("/register")
    def register_user():
        return "Register"

    return authentication_bp