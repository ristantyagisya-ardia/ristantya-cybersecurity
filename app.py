import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "database.db"

# --- Inisialisasi database ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Hello, Cyber Security with Database!"

@app.route("/add", methods=["POST"])
def add_message():
    data = request.json
    msg = data.get("msg", "")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (?)", (msg,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": msg})

@app.route("/list", methods=["GET"])
def list_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
