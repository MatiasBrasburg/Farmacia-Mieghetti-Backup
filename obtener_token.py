import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Datos que me pasaste
CLIENT_ID = "775773489646-h7s2p0mg6ntuukqvv1t6hqhsju4g2oi7.apps.googleusercontent.com"
CLIENT_SECRET = "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"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_refresh_token():
    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    # Esto abrirá el navegador para que autorices
    creds = flow.run_local_server(port=0)
    
    print("\n✅ ¡Autorización exitosa!")
    print(f"Tu REFRESH_TOKEN es: {creds.refresh_token}")
    print("\nCopiá ese código y pasámelo.")

if __name__ == "__main__":
    get_refresh_token()
