import base64
from nacl import public
import json
import sys

def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(base64.b64decode(public_key))
    seal_box = public.SealedBox(public_key)
    encrypted = seal_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

if __name__ == "__main__":
    pub_key = "PLt3aCClyoGX5lkz8O2YW8jywCcJHyLcFV+Chmn13iw="
    
    # Secret values
    db_url = "postgresql://postgres:rcKhqnrYUnODdHPgOkcgFgmkHkQPNinq@yamanote.proxy.rlwy.net:53058/railway"
    drive_id = "1vFDYJQUeA2dZ_bPmMzguZqj1fGyWqg6G"
    
    with open(r"C:\Users\Usuario\Downloads\automatizacion-back-ups-fa-4e423d63e8e6.json", "r") as f:
        google_json = f.read()
    
    # Encrypt and print
    print(f"DATABASE_URL_ENC={encrypt(pub_key, db_url)}")
    print(f"DRIVE_FOLDER_ID_ENC={encrypt(pub_key, drive_id)}")
    print(f"GOOGLE_SERVICE_ACCOUNT_JSON_ENC={encrypt(pub_key, google_json)}")
