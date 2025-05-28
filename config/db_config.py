import os
from config.env_config import test_env, env

def load_mongo_uri():
    if env == "test" and test_env == "github-actions":
        return os.getenv("MONGO_URI"), os.getenv("MONGO_DB")
    else:
        from config.secrets import MONGO_URI, MONGO_DB
        return MONGO_URI, MONGO_DB

MONGO_URI, MONGO_DB = load_mongo_uri()