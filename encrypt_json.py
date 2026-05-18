import base64
from nacl import public
import json

def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(base64.b64decode(public_key))
    seal_box = public.SealedBox(public_key)
    encrypted = seal_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

if __name__ == "__main__":
    pub_key = "PLt3aCClyoGX5lkz8O2YW8jywCcJHyLcFV+Chmn13iw="
    with open(r"C:\Users\Usuario\Downloads\automatizacion-back-ups-fa-4e423d63e8e6.json", "r") as f:
        content = f.read()
    print(encrypt(pub_key, content))
