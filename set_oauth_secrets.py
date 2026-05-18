import os
import requests
import base64
from nacl import public
import json

def encrypt(public_key: str, secret_value: str) -> str:
    public_key_obj = public.PublicKey(base64.b64decode(public_key))
    seal_box = public.SealedBox(public_key_obj)
    encrypted = seal_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def set_secret(owner, repo, token, secret_name, secret_value, key_id, public_key):
    encrypted_value = encrypt(public_key, secret_value)
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/secrets/{secret_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [201, 204]:
        print(f"✅ Secret {secret_name} set successfully.")
    else:
        print(f"❌ Failed to set secret {secret_name}: {response.status_code} {response.text}")

if __name__ == "__main__":
    owner = "MatiasBrasburg"
    repo = "Farmacia-Mieghetti-Backup"
    token = "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"
    key_id = "3380204578043523366"
    public_key = "PLt3aCClyoGX5lkz8O2YW8jywCcJHyLcFV+Chmn13iw="

    # OAuth2 Secrets
    client_id = "775773489646-h7s2p0mg6ntuukqvv1t6hqhsju4g2oi7.apps.googleusercontent.com"
    client_secret = "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"
    refresh_token = "1//0h0Kx9PV2WmcaCgYIARAAGBESNwF-L9IrbLve2OxkiNngFdoWJ7bJ3ZgZiKoPWzygDycMEus0iHsvllkIyQTW31PjanZEG6VqvOA"

    set_secret(owner, repo, token, "GOOGLE_CLIENT_ID", client_id, key_id, public_key)
    set_secret(owner, repo, token, "GOOGLE_CLIENT_SECRET", client_secret, key_id, public_key)
    set_secret(owner, repo, token, "GOOGLE_REFRESH_TOKEN", refresh_token, key_id, public_key)
