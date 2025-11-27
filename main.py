import telebot
import os
import json
from datetime import datetime

# -------------------------
# CONFIGURACIÓN
# -------------------------
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")      # reemplaza con el token de tu bot
ADMIN_ID = os.getenv("USER_ID")           # tu Telegram ID para recibir notificaciones
LOG_FILE = "logs.txt"
OFFSET_FILE = "offset.json"   # guardamos el offset para no procesar mensajes dos veces

bot = telebot.TeleBot(TOKEN, threaded=False)  # desactivamos threading para ejecución puntual

# -------------------------
# FUNCIONES AUXILIARES
# -------------------------
def get_offset():
    try:
        with open(OFFSET_FILE, "r") as f:
            data = json.load(f)
            return data.get("offset", 0)
    except FileNotFoundError:
        return 0

def save_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        json.dump({"offset": offset}, f)

def log_message(user, text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {user} | {text}"
    # Guardamos en el log local
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")
    # Te enviamos un aviso
    bot.send_message(ADMIN_ID, f"[LOG] {user} envió: {text}")

# -------------------------
# EJECUCIÓN
# -------------------------
def main():
    offset = get_offset()
    updates = bot.get_updates(offset=offset, timeout=0)

    for update in updates:
        update_id = update.update_id
        message = update.message
        if message:
            user = message.from_user.username or str(message.from_user.id)
            text = message.text or ""
            log_message(user, text)
        # actualizamos el offset para no procesarlo de nuevo
        offset = update_id + 1

    save_offset(offset)
    print(f"Procesados {len(updates)} mensajes. Offset guardado: {offset}")

if __name__ == "__main__":
    main()
