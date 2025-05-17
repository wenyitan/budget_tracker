import base64
def generate_basic_auth_headers(username, password):
    credentials = f"{username}:{password}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")
    header = {
        "Authorization": f"Basic {encoded_credentials}"
    }
    return header

def generate_token_header(token):
    header = {
        "Authorization": f"Bearer {token}"
    }
    return header