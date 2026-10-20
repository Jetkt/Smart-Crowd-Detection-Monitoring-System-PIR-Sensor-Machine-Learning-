import requests
from datetime import datetime

# ===============================
# TELEGRAM CONFIG
# ===============================
BOT_TOKEN = "8066437087:AAH2t2MIjhxzXYDw1jxmfmyTboaoklQeVyk"
CHAT_ID = "1139679922"

# ===============================
# STATUS MEMORY (ANTI SPAM)
# ===============================
last_status = None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("❌ Telegram Error:", e)


def notify_if_needed(pir, pred, confidence):
    global last_status

    status = "ADA ORANG" if pred == 1 else "TIDAK ADA ORANG"

    # ✅ Kirim hanya jika status berubah
    if status != last_status:
        last_status = status

        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icon = "🟥" if pred == 1 else "🟩"

        message = (
            f"{icon} <b>STATUS RUANGAN BERUBAH</b>\n\n"
            f"👤 Status : <b>{status}</b>\n"
            f"📡 PIR    : {pir}\n"
            f"🎯 Confidence : {round(confidence,3)}\n"
            f"🕒 Waktu : {waktu}"
        )

        send_telegram_message(message)
