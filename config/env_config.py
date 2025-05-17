import os

env=os.getenv("ENV", "prod")
app=os.getenv("APP", "bot")
test_username=os.getenv("TEST_USERNAME", "testUsername")
test_password=os.getenv("TEST_PASSWORD", "testPassword")