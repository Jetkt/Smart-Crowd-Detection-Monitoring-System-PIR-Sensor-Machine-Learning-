from flask import Flask, request, jsonify, render_template, send_file
import tensorflow as tf
import numpy as np
import sqlite3
from datetime import datetime
import pandas as pd
import csv
import os



# ===============================
# TELEGRAM
# ===============================
try:
    from tele import send_telegram_message
    from tele import notify_if_needed
    TELE_ENABLE = True
    print("✅ Telegram module loaded")
except Exception as e:
    TELE_ENABLE = False
    print("⚠ Telegram DISABLED:", e)

# ===============================
# CONFIG
# ===============================
MODEL_PATH = "crowded_model.h5"
DB_NAME = "crowded.db"

# ===============================
# INIT APP
# ===============================
app = Flask(__name__)

# ===============================
# LOAD MODEL
# ===============================
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model AI loaded:", MODEL_PATH)

# ===============================
# INIT DATABASE
# ===============================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS crowd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pir INTEGER,
            pred INTEGER,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ===============================
# SAVE TO DB
# ===============================
def save_to_db(pir, pred, confidence):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO crowd (pir, pred, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (pir, pred, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# ===============================
# API ESP32
# ===============================
@app.route("/send_data", methods=["POST"])
def receive_data():
    try:
        data = request.get_json(force=True)
        pir = int(data.get("pir", 0))

        prob = float(model.predict(np.array([[pir]]))[0][0])
        pred = 1 if prob >= 0.5 else 0

        save_to_db(pir, pred, prob)

        print(f"📡 PIR={pir} | PRED={pred} | CONF={round(prob,3)}")

        # ✅ TELEGRAM NOTIF
        if TELE_ENABLE:
            try:
                notify_if_needed(pir, pred, prob)
            except Exception as te:
                print("❌ Telegram error:", te)

        return jsonify({
            "pir": pir,
            "prediction": pred,
            "confidence": round(prob, 3),
            "status": "ADA_ORANG" if pred else "TIDAK_ADA_ORANG"
        })

    except Exception as e:
        print("❌ API Error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    data = request.get_json()

    # ✅ Safety Check
    if not data or "message" not in data:
        return "ok"

    message = data["message"]
    if "text" not in message:
        return "ok"

    text = message["text"].lower()


# ===============================
# API LATEST (DASHBOARD)
# ===============================
@app.route("/api/latest")
def api_latest():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        SELECT pir, pred, confidence, timestamp
        FROM crowd ORDER BY id DESC LIMIT 1
    """)
    row = cur.fetchone()
    conn.close()

    if not row:
        return jsonify({"status": "NO_DATA"})

    pir, pred, conf, time = row
    return jsonify({
        "pir": pir,
        "pred": pred,
        "confidence": round(conf, 3),
        "status": "ADA_ORANG" if pred else "TIDAK_ADA_ORANG",
        "timestamp": time
    })

# ===============================
# DASHBOARD
# ===============================
@app.route("/")
def dashboard():
    return render_template("index.html")

# ===============================
# EXPORT CSV
# ===============================
@app.route("/export")
def export_data():
    filename = "data_keramaian.csv"

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM crowd")
    rows = cur.fetchall()
    conn.close()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "PIR", "PRED", "CONFIDENCE", "TIMESTAMP"])
        writer.writerows(rows)

    return send_file(filename, as_attachment=True)

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False   # ❗ PENTING: debug FALSE untuk Telegram
    )
