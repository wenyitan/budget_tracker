from api.app_factory import create_app
from config.env_config import test_username, test_password
from tests.utils import generate_basic_auth_headers, generate_token_header
import pytest
from bot.transaction import Transaction

app = create_app()

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

class TestApiFlow:

    test_variables = {}

    def test_register(self, client):
        response = client.post("/api/v1/authentication/register", json={
            "username": test_username,
            "password": test_password
        })
        response_body = response.get_json()
        print("")
        print("API Response:", response_body)
        print("Asserting response status code == 201")
        assert response.status_code == 201
        print("=======================================================")

    def test_register_using_same_username(self, client):
        response = client.post("/api/v1/authentication/register", json={
            "username": test_username,
            "password": "test_password"
        })
        response_body = response.get_json()
        print("")
        print("API Response:", response_body)
        print("Asserting response status code == 409")
        assert response.status_code == 409
        expected_error_msg = 'Username already exists'
        print(f"Asserting response body error: {expected_error_msg}")
        assert response_body["error"] == expected_error_msg
        print("=======================================================")

    def test_generate_token(self, client):
        headers = generate_basic_auth_headers(test_username, test_password)
        response = client.get("/api/v1/authentication/generate-token", headers=headers)
        response_body = response.get_json()
        print("")
        print("Asserting response status code == 200")
        assert response.status_code == 200
        print("Asserting token valid for 24hrs or 86400 seconds")
        assert response_body['expiry'] == 86400
        print("Asserting 'token' is a key in response body")
        assert 'token' in response_body.keys()
        TestApiFlow.test_variables['token'] = response_body['token']
        print("=======================================================")

    def test_add_transaction(self, client):
        headers = generate_token_header(TestApiFlow.test_variables['token'])
        test_amount, test_person, test_date, test_description, test_category_id = 1.23, "testUser", "18-May-2025", "Bubble tea", 1
        transaction = Transaction(amount=test_amount, person=test_person, date=test_date, description=test_description, category_id=test_category_id)
        response = client.post("/api/v1/transactions/", headers=headers, json=transaction.__dict__)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 201")
        assert response.status_code == 201
        print(f"Asserting response body amount == {test_amount}")
        assert response_body["transaction"]["amount"] == test_amount
        print(f"Asserting response body person == {test_person}")
        assert response_body["transaction"]["person"] == test_person
        print(f"Asserting response body date == {test_date}")
        assert response_body["transaction"]["date"] == test_date
        print(f"Asserting response body description == {test_description}")
        assert response_body["transaction"]["description"] == test_description
        print(f"Asserting response body category_id == {test_category_id}")
        assert response_body["transaction"]["category_id"] == test_category_id
        print("=======================================================")

    def test_get_all_transactions(self, client):
        headers = generate_token_header(TestApiFlow.test_variables['token'])
        response = client.get("/api/v1/transactions/", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 200")
        assert response.status_code == 200
        transaction_ids = list(map(lambda transaction:transaction['id'], response_body))
        transaction_ids.sort()
        TestApiFlow.test_variables['transaction_ids'] = transaction_ids
        print("=======================================================")

    def test_get_transaction_by_id(self, client):
        headers = generate_token_header(TestApiFlow.test_variables['token'])
        id = TestApiFlow.test_variables['transaction_ids'][-1]
        response = client.get(f"/api/v1/transactions/{id}", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 200")
        assert response.status_code == 200
        print(f"Asserting transaction id == {id}")
        assert response_body['id'] == id
        print("=======================================================")

    def test_get_transaction_by_id_not_found(self, client):
        headers = generate_token_header(TestApiFlow.test_variables['token'])
        id = TestApiFlow.test_variables['transaction_ids'][-1] + 1
        response = client.get(f"/api/v1/transactions/{id}", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 404")
        assert response.status_code == 404
        print("=======================================================")

    def test_delete_user(self, client):
        headers = generate_basic_auth_headers(test_username, test_password)
        response = client.delete("/api/v1/authentication/delete-user", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 200")
        assert response.status_code == 200
        print("=======================================================")

    def test_delete_user_again(self, client):
        headers = generate_basic_auth_headers(test_username, test_password)
        response = client.delete("/api/v1/authentication/delete-user", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 401")
        assert response.status_code == 401
        expected_error_msg = 'Unauthorised access'
        print(f"Asserting response body error: {expected_error_msg}")
        assert response_body["error"] == expected_error_msg
        print("=======================================================")