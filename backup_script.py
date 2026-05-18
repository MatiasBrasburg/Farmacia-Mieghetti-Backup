import os
import subprocess
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json

# --- CONFIGURACIÓN ---
# Estos valores se deben configurar como "Secrets" en el repositorio de GitHub
DATABASE_URL = os.environ.get('DATABASE_URL')
DRIVE_FOLDER_ID = os.environ.get('DRIVE_FOLDER_ID') # El ID de la carpeta en Drive
SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON') # El JSON completo como string

def run_backup():
    try:
        # 1. Crear el nombre del archivo con la fecha
        date_str = datetime.datetime.now().strftime("%d-%m-%Y")
        backup_filename = f"{date_str}.sql"
        print(f"🚀 Iniciando backup: {backup_filename}")

        # 2. Ejecutar pg_dump usando la DATABASE_URL
        # Usamos la URL pública para que GitHub Actions pueda conectarse
        subprocess.run(['pg_dump', DATABASE_URL, '-f', backup_filename], check=True)
        print("✅ Dump de la base de datos completado.")

        # 3. Autenticarse con Google Drive
        creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
        creds = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=['https://www.googleapis.com/auth/drive.file']
        )
        service = build('drive', 'v3', credentials=creds)

        # 4. Subir el archivo a Google Drive
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

        # 5. Limpiar el archivo local
        os.remove(backup_filename)
        print("🗑️ Archivo local eliminado.")

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        exit(1)

if __name__ == "__main__":
    if not DATABASE_URL or not DRIVE_FOLDER_ID or not SERVICE_ACCOUNT_JSON:
        print("❌ Faltan variables de entorno (DATABASE_URL, DRIVE_FOLDER_ID o GOOGLE_SERVICE_ACCOUNT_JSON)")
        exit(1)
    run_backup()
