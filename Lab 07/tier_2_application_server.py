import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 5000
DB_HOST = "127.0.0.1"
DB_PORT = 6000

def forward_to_database(request_json):
    """Send JSON to database server and return JSON response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as db_sock:
        db_sock.connect((DB_HOST, DB_PORT))
        db_sock.send(json.dumps(request_json).encode("utf-8"))
        response = db_sock.recv(4096).decode("utf-8")
    return json.loads(response)

def handle_client(conn, addr):
    print(f"[APP] Connected to client {addr}")
    try:
        data = conn.recv(4096).decode("utf-8")
        if not data:
            return
        request = json.loads(data)

        # Check connection close by client
        if request.get("action") == "exit":
            conn.send(json.dumps({"from": "application_server", "status": "Disconnected"}).encode("utf-8"))
            conn.close()
            print(f"[APP] Disconnected from client {addr}")
            return

        # Pass request to database server
        db_response = forward_to_database(request)

        # Wrap response for client
        response = {"from": "application_server", "db_response": db_response}
        conn.send(json.dumps(response).encode("utf-8"))

    except Exception as e:
        conn.send(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
    finally:
        conn.close()
        print(f"[APP] Disconnected from client {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[APP] Application server running on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
