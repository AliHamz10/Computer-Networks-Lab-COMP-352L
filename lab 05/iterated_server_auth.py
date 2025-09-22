import socket

users = {}  # store credentials in memory (can be extended to a file)

def handle_client(conn):
    conn.send("Welcome! Would you like to (1) Register or (2) Login? ".encode())
    choice = conn.recv(1024).decode().strip()

    if choice == "1":
        conn.send("Username: ".encode())
        username = conn.recv(1024).decode().strip()

        conn.send("Password: ".encode())
        password = conn.recv(1024).decode().strip()

        conn.send("Retype password: ".encode())
        password2 = conn.recv(1024).decode().strip()

        if password == password2:
            users[username] = password
            conn.send(f"User '{username}' registered successfully!\n".encode())
        else:
            conn.send("Passwords do not match.\n".encode())
        return

    elif choice == "2":
        while True:
            conn.send("Username: ".encode())
            username = conn.recv(1024).decode().strip()

            if username not in users:
                conn.send("User unknown. Try again.\n".encode())
                continue

            conn.send("Password: ".encode())
            password = conn.recv(1024).decode().strip()

            if users[username] == password:
                conn.send(f"Welcome {username}!\n".encode())
                break
            else:
                conn.send("Password incorrect. Try again.\n".encode())

def start_server():
    host = "127.0.0.1"
    port = 9000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(3)

    print(f"[*] Auth Server started on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"[+] Connected by {addr}")
        handle_client(conn)
        conn.close()
        print("[-] Client disconnected.")

if __name__ == "__main__":
    start_server()
