import os
import subprocess
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import urllib.parse

# --- CONFIGURACIÓN ---
DATABASE_URL = os.environ.get('DATABASE_URL')
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID')
SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')

def run_backup():
    try:
        # 1. Preparar la URL (asegurar SSL)
        url = DATABASE_URL
        if 'sslmode' not in url:
            separator = '&' if '?' in url else '?'
            url += f"{separator}sslmode=require"
        
        # 2. Crear el nombre del archivo con la fecha
        date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        backup_filename = f"{date_str}.sql"
        print(f"🚀 Iniciando backup: {backup_filename}")

        # 3. Ejecutar pg_dump
        # Usamos env vars para pasar la password de forma más segura si es posible,
        # pero pg_dump acepta la URL completa.
        result = subprocess.run(['pg_dump', url, '-f', backup_filename], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ Error en pg_dump:\n{result.stderr}")
            raise Exception("pg_dump failed")

        print("✅ Dump de la base de datos completado.")

        # 4. Autenticarse con Google Drive
        creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=['https://www.googleapis.com/auth/drive.file']
        )
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
    if not DATABASE_URL or not DRIVE_FOLDER_ID or not SERVICE_ACCOUNT_JSON:
        print("❌ Faltan variables de entorno.")
        exit(1)
    run_backup()
