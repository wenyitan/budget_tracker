from api.app_factory import create_app
from tests.test_config import test_username, test_password
from tests.utils import generate_basic_auth_headers, generate_token_header
import pytest

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
        print("Response:", response_body)
        print("Asserting response status code == 201")
        assert response.status_code == 201

    def test_register_using_same_username(self, client):
        response = client.post("/api/v1/authentication/register", json={
            "username": test_username,
            "password": "test_password"
        })
        response_body = response.get_json()
        print("")
        print("Response:", response_body)
        print("Asserting response status code == 409")
        assert response.status_code == 409
        expected_error_msg = 'Username already exists'
        print(f"Asserting response body error: {expected_error_msg}")
        assert response_body["error"] == expected_error_msg

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

    def test_get_transaction_by_id_not_found(self, client):
        headers = generate_token_header(TestApiFlow.test_variables['token'])
        id = TestApiFlow.test_variables['transaction_ids'][-1] + 1
        response = client.get(f"/api/v1/transactions/{id}", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 404")
        assert response.status_code == 404

    def test_delete_user(self, client):
        headers = generate_basic_auth_headers(test_username, test_password)
        response = client.delete("/api/v1/authentication/delete-user", headers=headers)
        response_body = response.get_json()
        print("")
        print("Response: ", response_body)
        print("Asserting response status code == 200")
        assert response.status_code == 200

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