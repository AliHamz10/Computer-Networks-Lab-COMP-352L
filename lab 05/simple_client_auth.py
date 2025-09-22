import socket

def start_client():
    host = input("Enter server IP Address: ")
    port = int(input("Enter server Port: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        response = client_socket.recv(1024).decode()
        if not response:
            break
        print(f"[Server] {response}", end="")

        message = input("[Client] ")
        client_socket.send(message.encode())

        if "Welcome" in response or "registered successfully" in response:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
