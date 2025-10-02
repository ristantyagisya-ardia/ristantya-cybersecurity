import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = "database.db"

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


SECRET_KEY = "THIS_IS_A_SECRET_KEY_123456"

@app.route("/")
def home():
    return "Hello — testing code scanning alerts!"

@app.route("/add_insecure", methods=["POST"])
def add_insecure():
    data = request.json or {}
    # insecure: directly concatenating user input into SQL
    msg = data.get("msg", "")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    sql = "INSERT INTO messages (content) VALUES ('%s')" % msg
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({"status": "ok", "message": msg})


@app.route("/run_cmd")
def run_cmd():
    cmd = request.args.get("cmd", "echo hello")
    # insecure: running shell command from user input
    output = os.popen(cmd).read()
    return jsonify({"output": output})


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    # insecure: using eval on unsanitized input
    try:
        result = eval(expr)
    except Exception as e:
        result = str(e)
    return jsonify({"expr": expr, "result": str(result)})


@app.route("/save", methods=["POST"])
def save_file():
    data = request.json or {}
    content = data.get("content", "no content")
    path = "/tmp/insecure_saved_file.txt"
    with open(path, "w") as f:
        f.write(content)
    # set insecure permissions
    os.chmod(path, 0o777)
    return jsonify({"saved_to": path})

# safe-ish read endpoint (uses parameterized query)
@app.route("/list")
def list_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
