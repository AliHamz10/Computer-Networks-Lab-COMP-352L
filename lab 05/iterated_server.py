import socket

def start_server():
    host = "127.0.0.1"
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # backlog set to 3
    server_socket.listen(3)
    print(f"[*] Server started on {host}:{port}")

    client_count = 0

    while True:
        conn, addr = server_socket.accept()
        client_count += 1
        print(f"[+] Connected by {addr}")

        data = conn.recv(1024).decode()
        print(f"[Client {client_count}]: {data}")

        response = f"Connected to Client {client_count}"
        conn.send(response.encode())

        conn.close()
        print(f"[-] Client {client_count} disconnected.")

if __name__ == "__main__":
    start_server()
