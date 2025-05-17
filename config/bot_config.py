import os
import json
from config.env_config import test_env, env

DATE_FORMAT = "%d-%b-%Y"

def load_allowed_users():
    if env == "test" and test_env == "github-actions":
        return json.loads(os.getenv("allowed_users"))
    else:
        from config.secrets import ALLOWED_USERS
        return ALLOWED_USERS

ALLOWED_USERS = load_allowed_users()