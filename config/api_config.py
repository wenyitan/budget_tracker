import os
from config.env_config import test_env, env

def load_jwt_key():
    if env == "test" and test_env == "github-actions":
        return os.getenv("JWT_SECRET_KEY")
    else:
        from config.secrets import JWT_SECRET_KEY
        return JWT_SECRET_KEY

JWT_SECRET_KEY = load_jwt_key()