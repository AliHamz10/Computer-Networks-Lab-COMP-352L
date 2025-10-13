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
    create_students_table = """
    CREATE TABLE IF NOT EXISTS students (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gpa REAL
    );
    """
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """
    default_data = [
        ("1001", "Alice", 3.8),
        ("1002", "Bob", 3.5),
        ("1003", "Charlie", 3.9)
    ]
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(create_students_table)
    cur.execute(create_users_table)
    
    # Clear users table for testing purposes to ensure unique IDs can be registered
    cur.execute("DELETE FROM users")
    print("[DB] Cleared users table for testing")
    
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
        action = request.get("action")

        if action == "get_student":
            student_id = request.get("id")
            cur.execute("SELECT name, gpa FROM students WHERE id = ?", (student_id,))
            row = cur.fetchone()
            if row:
                response = {"status": "ok", "data": {"id": student_id, "name": row[0], "gpa": row[1]}}
            else:
                response = {"status": "error", "message": "Student not found"}
        
        elif action == "register":
            user_id = request.get("id")
            username = request.get("username")
            password = request.get("password")
            name = request.get("name")
            email = request.get("email")
            
            try:
                cur.execute("INSERT INTO users (id, username, password, name, email) VALUES (?, ?, ?, ?, ?)",
                           (user_id, username, password, name, email))
                conn_db.commit()
                response = {"status": "ok", "message": "User registered successfully"}
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed: users.username" in str(e):
                    response = {"status": "error", "message": "Username already exists"}
                elif "UNIQUE constraint failed: users.email" in str(e):
                    response = {"status": "error", "message": "Email already exists"}
                else:
                    response = {"status": "error", "message": "Registration failed: " + str(e)}
        
        elif action == "login":
            username = request.get("username")
            password = request.get("password")
            
            cur.execute("SELECT id, name, email FROM users WHERE username = ? AND password = ?", 
                       (username, password))
            row = cur.fetchone()
            if row:
                response = {"status": "ok", "data": {"id": row[0], "name": row[1], "email": row[2]}}
            else:
                response = {"status": "error", "message": "Invalid username or password"}
        
        else:
            response = {"status": "error", "message": "Unknown action"}

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
