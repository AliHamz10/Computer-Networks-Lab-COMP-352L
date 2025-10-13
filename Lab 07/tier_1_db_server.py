import socket
import threading
import sqlite3
import json
import os

HOST = "127.0.0.1"
PORT = 6000
DB_FILE = "students.db"

# Initialize database
def init_db():
    create_table = """
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gpa REAL
    );
    """
    default_data = [
        ("1001", "Alice", 3.8),
        ("1002", "Bob", 3.5),
        ("1003", "Charlie", 3.9)
    ]
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(create_table)
    cur.execute("SELECT COUNT(*) FROM students")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO students VALUES (?, ?, ?)", default_data)
    conn.commit()
    conn.close()

def handle_request(conn, addr):
    print(f"[DB] Connection from {addr}")
    conn_db = sqlite3.connect(DB_FILE)
    cur = conn_db.cursor()
    try:
        data = conn.recv(4096).decode("utf-8")
        if not data:
            return

        request = json.loads(data)
        #action = request.get("action")

        
        student_id = request.get("id")
        cur.execute("SELECT name, gpa FROM students WHERE id = ?", (student_id,))
        row = cur.fetchone()
        if row:
            response = {"status": "ok", "data": {"id": student_id, "name": row[0], "gpa": row[1]}}
        else:
            response = {"status": "error", "message": "Student not found"}

        conn.send(json.dumps(response).encode("utf-8"))


    except Exception as e:
        conn.send(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
    finally:
        conn_db.close()
        conn.close()
        print(f"[DB] Closed connection with {addr}")

def main():
    init_db()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[DB] Database server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_request, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
