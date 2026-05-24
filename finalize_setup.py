import os
import requests
import datetime
import time

# --- CONFIGURACIÓN ---
# Usamos la Green API que ya tienes configurada para el bot de Viken
INSTANCE_ID = "7103525050"
TOKEN = "97f6947c4156485892813fbcc53c033cac597c8a9a494c24ab"
PHONE_NUMBER = "5491155841206"
TARGET_DATE = "14-07-2026" # Fecha de las vacaciones de invierno

def send_whatsapp(message):
    url = f"https://7103.api.greenapi.com/waInstance{INSTANCE_ID}/sendMessage/{TOKEN}"
    payload = {
        "chatId": f"{PHONE_NUMBER}@c.us",
        "message": message
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 200

def check_and_send():
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    if today == TARGET_DATE:
        msg = "🚀 ¡Hola Mati! Soy tu bot. ¡Arrancaron las vacaciones de invierno! ¿Hacemos el script de los atajos mágicos (/cbu, etc.) que planeamos?"
        if send_whatsapp(msg):
            print("✅ Mensaje recordatorio enviado con éxito.")
            return True
    return False

if __name__ == "__main__":
    check_and_send()
# Last Sync Check: $(Get-Date)
