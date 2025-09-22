import socket

def start_server():
    host = "127.0.0.1"
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)

    print(f"[*] Echo Server started on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"[+] Connected by {addr}")
        conn.send("Connection Established.".encode())

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.lower() == "disconnect":
                conn.send("Connection terminated.".encode())
                conn.close()
                print("[-] Client disconnected.")
                break
            else:
                response = f"{data} (Echoed)"
                conn.send(response.encode())

if __name__ == "__main__":
    start_server()
