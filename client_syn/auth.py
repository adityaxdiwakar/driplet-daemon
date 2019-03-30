import requests


def verify_url(client_id):
    return f"http://localhost:3141/endpoints/accounts/{client_id}/verify"


def verify(client_id, token):
    r = requests.get(verify_url(client_id), headers={"authorization": token})
    if r.status_code == 200:
        return True
    return False
