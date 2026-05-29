import os
import subprocess
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import urllib.parse

# --- CONFIGURACIÓN ---
DATABASE_URL = os.environ.get('DATABASE_URL')
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID')

# OAuth2 Credentials
CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.environ.get('GOOGLE_REFRESH_TOKEN')

def run_backup():
    try:
        # 1. Parsear la DATABASE_URL
        parsed = urllib.parse.urlparse(DATABASE_URL)
        db_user = parsed.username
        db_password = parsed.password
        
        # DEBUG: Ver qué llega de las variables de entorno
        env_host = os.environ.get('PGHOST')
        env_port = os.environ.get('PGPORT')
        print(f"DEBUG: PGHOST env: {env_host}")
        print(f"DEBUG: PGPORT env: {env_port}")
        print(f"DEBUG: URL hostname: {parsed.hostname}")

        # Priorizamos variables de entorno individuales si existen (para el proxy público de Railway)
        db_host = env_host or parsed.hostname
        db_port = env_port or str(parsed.port)
        db_name = parsed.path.lstrip('/')

        # 2. Crear el nombre del archivo con la fecha
        date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        backup_filename = f"{date_str}.sql"
        print(f"🚀 Iniciando backup: {backup_filename}")

        # 3. Ejecutar pg_dump con PGPASSWORD
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password
        
        # Agregamos parámetros de timeout y quitamos cualquier forzado de SSL manual
        # ya que Railway proxy a veces se marea con eso.
        cmd = [
            'pg_dump',
            '--no-owner',
            '--no-privileges',
            '-h', db_host,
            '-p', db_port,
            '-U', db_user,
            '-f', backup_filename,
            db_name
        ]
        
        print(f"📡 Intentando conectar a {db_host}:{db_port} (User: {db_user}, DB: {db_name})...")
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error en pg_dump (Código {result.returncode}):")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            raise Exception("pg_dump failed")

        print("✅ Dump de la base de datos completado.")

        # 4. Autenticarse con Google Drive usando OAuth2 Refresh Token
        creds = Credentials(
            None,
            refresh_token=REFRESH_TOKEN,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        if not creds.valid:
            creds.refresh(Request())
            
        service = build('drive', 'v3', credentials=creds)

        # 5. Subir el archivo a Google Drive
        file_metadata = {
            'name': backup_filename,
            'parents': [DRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(backup_filename, mimetype='application/sql')
        
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        print(f"✅ Backup subido a Drive con ID: {uploaded_file.get('id')}")

        # 6. Limpiar el archivo local
        os.remove(backup_filename)
        print("🗑️ Archivo local eliminado.")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        exit(1)

if __name__ == "__main__":
    if not all([DATABASE_URL, DRIVE_FOLDER_ID, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("❌ Faltan variables de entorno.")
        exit(1)
    run_backup()
