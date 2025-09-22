import socket
import threading

def handle_client(conn, addr, client_count):
    """Handle individual client connection"""
    try:
        print(f"[+] Client {client_count} connected from {addr}")
        
        data = conn.recv(1024).decode()
        print(f"[Client {client_count}]: {data}")

        response = f"Connected to Client {client_count}"
        conn.send(response.encode())
        
        print(f"[-] Client {client_count} disconnected.")
    except Exception as e:
        print(f"Error handling client {client_count}: {e}")
    finally:
        conn.close()

def start_server():
    host = "127.0.0.1"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    # backlog set to 3
    server_socket.listen(3)
    print(f"[*] Server started on {host}:{port}")
    print(f"[*] Backlog set to 3 - can queue up to 3 pending connections")
    print(f"[*] Waiting for connections...")

    client_count = 0

    while True:
        conn, addr = server_socket.accept()
        client_count += 1
        
        # Create a new thread for each client
        client_thread = threading.Thread(
            target=handle_client, 
            args=(conn, addr, client_count)
        )
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":
    start_server()
