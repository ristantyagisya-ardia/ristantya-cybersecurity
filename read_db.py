import sqlite3

DB_NAME = "database.db"

def read_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    messages = read_messages()
    if not messages:
        print("Database kosong.")
    else:
        print("Isi database:")
        for row in messages:
            print(f"ID: {row[0]}, Content: {row[1]}")
